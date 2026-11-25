from collections import defaultdict

from metamodel.core.Cardinality import Cardinality
from metamodel.core.Registry import Registry
from metamodel.core.ValidationReport import ValidationReport


def validateCardinalities(model) -> ValidationReport:
    """Validate cardinalities for all registered relationship types.

    Missing relationships count as zero. The target cardinality
    constrains outgoing relationships per source entity, while the
    source cardinality constrains incoming relationships per target entity.
    """
    report = ValidationReport()

    entities = model.entities
    relationships = model.relationships

    relationships_by_type = defaultdict(list)

    for rel in relationships:
        relationships_by_type[rel.__class__].append(rel)

    relationship_classes = Registry.load_default().get_relationship_classes()

    for rel_cls in relationships_by_type:
        if rel_cls not in relationship_classes:
            relationship_classes.append(rel_cls)

    for rel_cls in relationship_classes:
        rels = relationships_by_type.get(rel_cls, [])

        source_card = Cardinality.parse(
            getattr(rel_cls, "source_cardinality", None)
        )
        target_card = Cardinality.parse(
            getattr(rel_cls, "target_cardinality", None)
        )
        source_type = getattr(rel_cls, "source_type", None)
        target_type = getattr(rel_cls, "target_type", None)

        check_outgoing = (
            target_card is not None and source_type is not None
        )
        check_incoming = (
            source_card is not None and target_type is not None
        )

        outgoing = defaultdict(int)
        incoming = defaultdict(int)

        if check_outgoing or check_incoming:
            for rel in rels:
                if check_outgoing:
                    outgoing[rel.source_entity.id] += 1
                if check_incoming:
                    incoming[rel.target_entity.id] += 1

        if check_outgoing:
            for entity in entities:
                if isinstance(entity, source_type):
                    count = outgoing.get(entity.id, 0)

                    if not target_card.contains(count):
                        report.add_error(
                            "cardinalityValidator",
                            f"{rel_cls.__name__}: {entity.type} "
                            f"{entity.name!r} has {count} target "
                            f"relationship(s); expected {target_card}.",
                        )

        if check_incoming:
            for entity in entities:
                if isinstance(entity, target_type):
                    count = incoming.get(entity.id, 0)

                    if not source_card.contains(count):
                        report.add_error(
                            "cardinalityValidator",
                            f"{rel_cls.__name__}: {entity.type} "
                            f"{entity.name!r} has {count} source "
                            f"relationship(s); expected {source_card}.",
                        )

    connected_ids = set()

    for rel in relationships:
        connected_ids.add(rel.source_entity.id)
        connected_ids.add(rel.target_entity.id)

    for entity in entities:
        if entity.id not in connected_ids:
            report.add_warning(
                "cardinalityValidator",
                f"{entity.type} {entity.name!r} is isolated.",
            )
    return report
