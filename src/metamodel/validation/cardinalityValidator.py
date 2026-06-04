from collections import defaultdict

from metamodel.core.Cardinality import Cardinality
from metamodel.core.ValidationReport import ValidationReport


def validateCardinalities(model) -> ValidationReport:
    """Validate multiplicities for all relationship instances.

    The label near the target side is interpreted as the number of target instances
    allowed for each source instance. The label near the source side is interpreted
    as the number of source instances allowed for each target instance.
    """
    report = ValidationReport()
    relationship_types = {rel.__class__ for rel in model.relationships}

    for rel_cls in relationship_types:
        rels = [rel for rel in model.relationships if isinstance(rel, rel_cls)]
        source_card = Cardinality.parse(getattr(rel_cls, "source_cardinality", None))
        target_card = Cardinality.parse(getattr(rel_cls, "target_cardinality", None))
        source_type = getattr(rel_cls, "source_type", None)
        target_type = getattr(rel_cls, "target_type", None)

        if target_card is not None and source_type is not None:
            outgoing = defaultdict(int)
            for rel in rels:
                outgoing[rel.source_entity.id] += 1
            for entity in model.entities:
                if isinstance(entity, source_type):
                    count = outgoing[entity.id]
                    if not target_card.contains(count):
                        report.add_error(
                            "cardinalityValidator",
                            f"{rel_cls.__name__}: {entity.type} {entity.name!r} has {count} target relationship(s); expected {target_card}.",
                        )

        if source_card is not None and target_type is not None:
            incoming = defaultdict(int)
            for rel in rels:
                incoming[rel.target_entity.id] += 1
            for entity in model.entities:
                if isinstance(entity, target_type):
                    count = incoming[entity.id]
                    if not source_card.contains(count):
                        report.add_error(
                            "cardinalityValidator",
                            f"{rel_cls.__name__}: {entity.type} {entity.name!r} has {count} source relationship(s); expected {source_card}.",
                        )
    return report
