import pytest

from metamodel.core.Model import Model
from metamodel.core.Registry import Registry

from metamodel.validation.referenceValidator import validateReferences
from metamodel.validation.typeValidator import validateTypes
from metamodel.validation.cardinalityValidator import validateCardinalities

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType
from metamodel.infrastructure.entities.Application import Application
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability
from metamodel.cyberThreat.entities.HumanVulnerability import HumanVulnerability
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise

from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.basedIn import basedIn
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.hasNodeType import hasNodeType
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.exploitsVulnerability import exploitsVulnerability
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise


# Reference Validator tests


def test_valid_references():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    model.add(operatesIn(org, sector))
    report = validateReferences(model)
    assert report.is_valid
    assert report.messages == []


def test_missing_source_reference():
    model = Model()
    org = Organization(name="Example")
    sector = model.add(Sector(name="Finance"))
    rel = operatesIn(org, sector)
    model._relationships.append(rel)
    report = validateReferences(model)
    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "referenceValidator"
    assert "source entity not present" in report.errors[0].message
    assert rel.id in report.errors[0].message


def test_missing_target_reference():
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = Sector(name="Finance")
    rel = operatesIn(org, sector)
    model._relationships.append(rel)
    report = validateReferences(model)
    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "referenceValidator"
    assert "target entity not present" in report.errors[0].message
    assert rel.id in report.errors[0].message


def test_missing_both_references():
    model = Model()
    org = Organization(name="Example")
    sector = Sector(name="Finance")
    rel = operatesIn(org, sector)
    model._relationships.append(rel)
    report = validateReferences(model)
    assert not report.is_valid
    assert len(report.errors) == 2
    assert all(
        error.validator == "referenceValidator"
        for error in report.errors
    )
    assert any(
        "source entity not present" in error.message
        for error in report.errors
    )
    assert any(
        "target entity not present" in error.message
        for error in report.errors
    )
    assert all(
        rel.id in error.message
        for error in report.errors
    )


# Type Validator tests


@pytest.mark.parametrize("invalid_source, invalid_target", [
    (False, False),
    (True, False),
    (False, True),
    (True, True),
])
def test_endpoint_types(invalid_source, invalid_target):
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel = model.add(operatesIn(org, sector))
    expected = []
    if invalid_source:
        rel._source_entity = sector
        expected.append("operatesIn has invalid source type Sector.")
    if invalid_target:
        rel._target_entity = org
        expected.append("operatesIn has invalid target type Organization.")
    report = validateTypes(model)
    assert report.is_valid == (not expected)
    assert [error.message for error in report.errors] == expected
    assert all(
        error.validator == "typeValidator"
        for error in report.errors
    )
    assert report.warnings == []


@pytest.mark.parametrize("roles", [
    ("source",),
    ("target",),
    ("source", "target"),
])
def test_undefined_endpoint_types(roles, monkeypatch):
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    model.add(operatesIn(org, sector))
    for role in roles:
        monkeypatch.setattr(operatesIn, f"{role}_type", None)
    report = validateTypes(model)
    assert not report.is_valid
    assert [error.message for error in report.errors] == [
        f"operatesIn has undefined {role}_type."
        for role in roles
    ]
    assert all(
        error.validator == "typeValidator"
        for error in report.errors
    )


@pytest.mark.parametrize("role", ["source", "target"])
@pytest.mark.parametrize("value", [None, "invalid"])
def test_non_entity_endpoint(role, value):
    model = Model()
    org = model.add(Organization(name="Example"))
    sector = model.add(Sector(name="Finance"))
    rel = model.add(operatesIn(org, sector))
    setattr(rel, f"_{role}_entity", value)
    report = validateTypes(model)
    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "typeValidator"
    assert report.errors[0].message == (
        f"operatesIn has invalid {role} type {type(value).__name__}."
    )


@pytest.mark.parametrize("vulnerability_class", [
    Vulnerability,
    SoftwareVulnerability,
    ConfigVulnerability,
    HumanVulnerability,
])
def test_vulnerability_subtypes(vulnerability_class):
    model = Model()
    step = model.add(ThreatStep(name="Example step"))
    vulnerability = model.add(
        vulnerability_class(name="Example vulnerability")
    )
    model.add(exploits(step, vulnerability))
    report = validateTypes(model)
    assert report.is_valid
    assert report.messages == []


# Cardinality Validator tests


@pytest.mark.parametrize("type_count, links, expected", [
    (1, [(0, 0), (1, 0)], []),

    (2, [(0, 0), (1, 1)], []),

    (1, [(0, 0)], [
        "hasNodeType: Node 'N2' has 0 target relationship(s); expected 1.",
    ]),

    (2, [(0, 0), (1, 0)], [
        "hasNodeType: NodeType 'T2' has 0 source relationship(s); expected 1..*.",
    ]),

    (2, [(0, 0), (0, 1), (1, 0)], [
        "hasNodeType: Node 'N1' has 2 target relationship(s); expected 1.",
    ]),

    (3, [(0, 0), (0, 1)], [
        "hasNodeType: Node 'N1' has 2 target relationship(s); expected 1.",
        "hasNodeType: Node 'N2' has 0 target relationship(s); expected 1.",
        "hasNodeType: NodeType 'T3' has 0 source relationship(s); expected 1..*.",
    ]),
])
def test_has_node_type_cardinalities(type_count, links, expected):
    model = Model()
    nodes = [
        model.add(Node(name=f"N{i + 1}"))
        for i in range(2)
    ]
    types = [
        model.add(NodeType(name=f"T{i + 1}"))
        for i in range(type_count)
    ]
    for source, target in links:
        model.add(hasNodeType(nodes[source], types[target]))
    report = validateCardinalities(model)
    node_type_errors = [
        error.message
        for error in report.errors
        if error.message.startswith("hasNodeType:")
    ]
    assert sorted(node_type_errors) == sorted(expected)
    assert all(
        error.validator == "cardinalityValidator"
        for error in report.errors
    )


@pytest.mark.parametrize("extra_country", [False, True])
def test_partially_unspecified_cardinality(extra_country):
    model = Model()
    org = model.add(Organization(name="Org"))
    model.add(Organization(name="Other org"))
    for name in ("Italy", "France"):
        country = model.add(HomeCountry(name=name))
        model.add(basedIn(org, country))
    if extra_country:
        model.add(HomeCountry(name="Germany"))
    report = validateCardinalities(model)
    based_in_errors = [
        error.message
        for error in report.errors
        if error.message.startswith("basedIn:")
    ]
    assert based_in_errors == ([
        "basedIn: HomeCountry 'Germany' has 0 source relationship(s); expected 1."
    ] if extra_country else [])

    assert all(
        error.validator == "cardinalityValidator"
        for error in report.errors
    )


def test_unspecified_cardinalities():
    model = Model()
    step = model.add(ThreatStep(name="Step"))
    model.add(ThreatStep(name="Other step"))
    for name in ("V1", "V2"):
        vulnerability = model.add(Vulnerability(name=name))
        model.add(exploits(step, vulnerability))
    model.add(Vulnerability(name="V3"))
    report = validateCardinalities(model)
    exploits_errors = [
        error.message
        for error in report.errors
        if error.message.startswith("exploits:")
    ]
    assert exploits_errors == []


@pytest.mark.parametrize("linked", [True, False])
def test_cardinality_with_entity_inheritance(linked):
    model = Model()
    ttp = model.add(TTP(name="Technique 1"))
    vulnerability = model.add(Vulnerability(name="Generic"))
    model.add(exploitsVulnerability(ttp, vulnerability))
    software = model.add(
        SoftwareVulnerability(name="Software")
    )
    if linked:
        second_ttp = model.add(TTP(name="Technique 2"))
        model.add(exploitsVulnerability(second_ttp, software))
    report = validateCardinalities(model)
    vulnerability_errors = [
        error.message
        for error in report.errors
        if error.message.startswith("exploitsVulnerability:")
    ]
    assert vulnerability_errors == (
        [] if linked else [
            "exploitsVulnerability: SoftwareVulnerability 'Software' "
            "has 0 source relationship(s); expected 1..*."
        ]
    )


@pytest.mark.parametrize("entity_class, expected_relations", [
    (
        Organization,
        {"operatesIn", "manages", "hasBusinessRequirement"},
    ),
    (
        Threat,
        {"threatPartOf", "initiates", "startsWith"},
    ),
])
def test_missing_mandatory_relations_across_domains(
    entity_class, expected_relations
):
    model = Model()
    model.add(entity_class(name="Example"))

    report = model.validate()

    assert not report.is_valid

    assert {
        error.message.split(":", 1)[0]
        for error in report.errors
    } == expected_relations

    assert len(report.errors) == len(expected_relations)

    assert all(
        error.validator == "cardinalityValidator"
        for error in report.errors
    )


# Model validation integration tests


def test_model_validation_valid(monkeypatch):
    monkeypatch.setattr(
        Registry,
        "get_relationship_classes",
        lambda self: [madeBy, hasNodeType],
    )
    model = Model()
    infrastructure = model.add(Infrastructure(name="Infra"))
    node = model.add(Node(name="N1"))
    node_type = model.add(NodeType(name="T1"))
    model.add(madeBy(infrastructure, node))
    model.add(hasNodeType(node, node_type))
    report = model.validate()
    assert report.is_valid
    assert report.messages == []


@pytest.mark.parametrize("reference_error, type_error", [
    (False, False),
    (True, False),
    (False, True),
    (True, True),
])
def test_model_validation_stages(monkeypatch, reference_error, type_error):
    monkeypatch.setattr(
        Registry,
        "get_relationship_classes",
        lambda self: [hasNodeType],
    )
    model = Model()
    expected = []
    node = model.add(Node(name="N1"))
    model.add(Node(name="N2"))
    node_type = model.add(NodeType(name="T1"))
    model.add(hasNodeType(node, node_type))
    step = model.add(ThreatStep(name="Step"))
    vulnerability = model.add(Vulnerability(name="V1"))
    if reference_error:
        external = Vulnerability(name="External")
        missing_reference = exploits(step, external)
        model._relationships.append(missing_reference)

        expected.append((
            "referenceValidator",
            f"Relationship {missing_reference.id} "
            "has a target entity not present in the model.",
        ))
    if type_error:
        wrong_type = model.add(exploits(step, vulnerability))
        wrong_type._target_entity = node_type

        expected.append((
            "typeValidator",
            "exploits has invalid target type NodeType.",
        ))
    if not reference_error and not type_error:
        expected.append((
            "cardinalityValidator",
            "hasNodeType: Node 'N2' has 0 target "
            "relationship(s); expected 1.",
        ))
    report = model.validate()
    assert not report.is_valid
    assert sorted(
        (error.validator, error.message)
        for error in report.errors
    ) == sorted(expected)
    expected_warnings = (
        [
            "Node 'N2' is isolated.",
            "ThreatStep 'Step' is isolated.",
            "Vulnerability 'V1' is isolated.",
        ]
        if not reference_error and not type_error
        else []
    )
    assert sorted(
        warning.message for warning in report.warnings
    ) == sorted(expected_warnings)


@pytest.mark.parametrize("role, endpoint", [
    ("source", None),
    ("target", None),
    ("source", "invalid"),
    ("target", "invalid"),
])
def test_model_validation_invalid_endpoint(role, endpoint):
    model = Model()

    node = model.add(Node(name="N1"))
    node_type = model.add(NodeType(name="T1"))

    rel = model.add(hasNodeType(node, node_type))

    setattr(rel, f"_{role}_entity", endpoint)

    report = model.validate()

    assert not report.is_valid
    assert len(report.errors) == 1

    error = report.errors[0]

    assert error.validator == "typeValidator"
    assert error.message == (
        f"hasNodeType has invalid {role} "
        f"type {type(endpoint).__name__}."
    )

    assert report.warnings == []


def test_missing_relations_and_isolation():
    model = Model()
    model.add(Node(name="N1"))
    report = model.validate()
    assert not report.is_valid
    assert len(report.errors) == 5
    assert {
        error.message.split(":", 1)[0]
        for error in report.errors
    } == {
        "madeBy",
        "hasNodeType",
        "hostsResource",
        "exposesPort",
        "runsOS",
    }
    assert all(
        error.validator == "cardinalityValidator"
        for error in report.errors
    )
    assert len(report.warnings) == 1
    assert report.warnings[0].message == (
        "Node 'N1' is isolated."
    )


def test_isolated_entity_warning_only():
    model = Model()
    model.add(Application(name="Standalone Application"))
    report = model.validate()
    assert report.is_valid
    assert report.errors == []
    assert len(report.warnings) == 1
    assert report.warnings[0].validator == "cardinalityValidator"
    assert report.warnings[0].message == (
        "Application 'Standalone Application' is isolated."
    )


def test_empty_model_is_valid():
    model = Model()
    report = model.validate()
    assert report.is_valid
    assert report.errors == []
    assert len(report.warnings) == 1
    assert report.warnings[0].validator == "modelValidator"
    assert report.warnings[0].message == (
        "Model is empty: no entities or relationships to validate."
    )


def test_disconnected_subgraphs_are_valid():
    model = Model()
    actor1 = model.add(ThreatActor(name="Actor 1"))
    expertise1 = model.add(Expertise(name="Expertise 1"))
    actor2 = model.add(ThreatActor(name="Actor 2"))
    expertise2 = model.add(Expertise(name="Expertise 2"))
    model.add(hasExpertise(actor1, expertise1))
    model.add(hasExpertise(actor2, expertise2))
    report = model.validate()
    assert report.is_valid
    assert report.errors == []
    assert report.warnings == []


def test_structural_errors_skip_cardinalities_with_real_registry():
    model = Model()
    model.add(Node(name="Orphan node"))
    step = model.add(ThreatStep(name="Step"))
    vulnerability = model.add(Vulnerability(name="V1"))
    rel = model.add(exploits(step, vulnerability))
    rel._target_entity = Node(name="External node")
    report = model.validate()
    assert not report.is_valid
    assert len(report.errors) == 2
    assert {
        (error.validator, error.message)
        for error in report.errors
    } == {
        (
            "referenceValidator",
            f"Relationship {rel.id} has a target "
            "entity not present in the model.",
        ),
        (
            "typeValidator",
            "exploits has invalid target type Node.",
        ),
    }
    assert report.warnings == []