from collections import defaultdict

from metamodel.core.Cardinality import Cardinality
from metamodel.core.Registry import Registry
from metamodel.core.ValidationReport import ValidationReport


def _union_cardinality(cards: list[Cardinality]) -> Cardinality:
    minimum = max(card.minimum for card in cards)
    if any(card.maximum is None for card in cards):
        return Cardinality(minimum, None)
    return Cardinality(minimum, max(minimum, sum(card.maximum for card in cards)))


def validateCardinalities(model) -> ValidationReport:
    """Validate cardinalities for all registered relationship types.

    Missing relationships count as zero. The target cardinality
    constrains outgoing relationships per source entity, while the
    source cardinality constrains incoming relationships per target entity.

    Two refinements follow the metamodel:

    * a metamodel association with several target types (e.g. ``affects`` from
      SoftwareVulnerability to OS and to Application) is implemented by one class
      per target type sharing the same ``label`` and source type; its target
      cardinality is checked on the union of these classes (e.g. a software
      vulnerability affects at least one OS or application);
    * ``cardinality_counts`` lists other relationship classes whose instances also
      count, e.g. application and OS instances run by a node count as resources it hosts.
    """
    report = ValidationReport()

    entities = model.entities
    relationships = model.relationships

    relationships_by_name = defaultdict(list)
    for rel in relationships:
        relationships_by_name[rel.__class__.__name__].append(rel)

    relationship_classes = Registry.load_default().get_relationship_classes()
    for rel in relationships:
        if rel.__class__ not in relationship_classes:
            relationship_classes.append(rel.__class__)

    def counted(rel_cls):
        names = (rel_cls.__name__,) + tuple(getattr(rel_cls, "cardinality_counts", ()))
        return [rel for name in names for rel in relationships_by_name.get(name, [])]

    # Group classes sharing label and source type (one UML association).
    groups = defaultdict(list)
    for rel_cls in relationship_classes:
        label = rel_cls.get_label() if hasattr(rel_cls, "get_label") else rel_cls.__name__
        groups[(label, rel_cls.source_type)].append(rel_cls)

    def check(entity_type, card, counts, message):
        for entity in entities:
            if isinstance(entity, entity_type):
                count = counts.get(entity.id, 0)
                if not card.contains(count):
                    report.add_error("cardinalityValidator", message(entity, count, card))

    for (label, source_type), classes in groups.items():
        # outgoing (target cardinality), per association
        target_cards = [Cardinality.parse(getattr(c, "target_cardinality", None)) for c in classes]
        if source_type is not None and all(card is not None for card in target_cards):
            card = target_cards[0] if len(classes) == 1 else _union_cardinality(target_cards)
            outgoing = defaultdict(int)
            for rel_cls in classes:
                for rel in counted(rel_cls):
                    outgoing[rel.source_entity.id] += 1
            name = classes[0].__name__ if len(classes) == 1 else label
            check(source_type, card, outgoing,
                  lambda e, n, c: f"{name}: {e.type} {e.name!r} has {n} target relationship(s); expected {c}.")

        # incoming (source cardinality), per class
        for rel_cls in classes:
            source_card = Cardinality.parse(getattr(rel_cls, "source_cardinality", None))
            target_type = getattr(rel_cls, "target_type", None)
            if source_card is None or target_type is None:
                continue
            incoming = defaultdict(int)
            for rel in counted(rel_cls):
                incoming[rel.target_entity.id] += 1
            check(target_type, source_card, incoming,
                  lambda e, n, c, r=rel_cls: f"{r.__name__}: {e.type} {e.name!r} has {n} source relationship(s); expected {c}.")

    connected_ids = set()
    for rel in relationships:
        connected_ids.add(rel.source_entity.id)
        connected_ids.add(rel.target_entity.id)
        connected_ids.update(ref.id for ref in rel.referenced_entities())

    for entity in entities:
        if entity.id not in connected_ids:
            report.add_warning(
                "cardinalityValidator",
                f"{entity.type} {entity.name!r} is isolated.",
            )
    return report
