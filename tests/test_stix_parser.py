from metamodel.io.stixParser import parseStixBundleWithReport
from metamodel.io.stix.generic import GenericStixObject, GenericStixRelationship
from metamodel.io.stix.constants import STIX_DOMAIN_OBJECT_TYPES, STIX_RELATIONSHIP_OBJECT_TYPES


def test_stix_parser_accepts_all_official_sdos_as_entities():
    objects = []
    for index, stix_type in enumerate(STIX_DOMAIN_OBJECT_TYPES, start=1):
        objects.append(
            {
                "type": stix_type,
                "spec_version": "2.1",
                "id": f"{stix_type}--00000000-0000-4000-8000-{index:012d}",
                "created": "2026-01-01T00:00:00.000Z",
                "modified": "2026-01-01T00:00:00.000Z",
                "name": f"Example {stix_type}",
            }
        )

    result = parseStixBundleWithReport({"type": "bundle", "id": "bundle--test", "objects": objects})

    assert len(result.model.entities) == len(STIX_DOMAIN_OBJECT_TYPES)
    assert result.skipped_objects == []


def test_stix_parser_maps_relationship_sro():
    bundle = {
        "type": "bundle",
        "id": "bundle--test",
        "objects": [
            {
                "type": "identity",
                "id": "identity--11111111-1111-4111-8111-111111111111",
                "name": "A",
            },
            {
                "type": "identity",
                "id": "identity--22222222-2222-4222-8222-222222222222",
                "name": "B",
            },
            {
                "type": "relationship",
                "id": "relationship--33333333-3333-4333-8333-333333333333",
                "relationship_type": "related-to",
                "source_ref": "identity--11111111-1111-4111-8111-111111111111",
                "target_ref": "identity--22222222-2222-4222-8222-222222222222",
            },
        ],
    }

    result = parseStixBundleWithReport(bundle)

    assert len(result.model.relationships) == 1
    assert isinstance(result.model.relationships[0], GenericStixRelationship)
    assert result.model.relationships[0].stix_relationship_type == "related-to"


def test_stix_parser_preserves_unknown_custom_objects():
    result = parseStixBundleWithReport(
        {
            "type": "bundle",
            "id": "bundle--test",
            "objects": [
                {
                    "type": "x-custom-object",
                    "id": "x-custom-object--11111111-1111-4111-8111-111111111111",
                    "name": "Custom",
                }
            ],
        }
    )

    assert len(result.model.entities) == 1
    assert isinstance(result.model.entities[0], GenericStixObject)
    assert result.model.entities[0].stix_type == "x-custom-object"
