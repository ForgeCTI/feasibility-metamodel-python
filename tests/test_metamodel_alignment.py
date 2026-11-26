"""The Python metamodel matches the paper (entities, relationships, multiplicities, new elements)."""
import pytest

from metamodel.core.Model import Model
from metamodel.core.Registry import Registry
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Code import Code
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.Data import Data
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.PrivilegeLevel import PrivilegeLevel
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.rels.grantsAccessToNode import grantsAccessToNode
from metamodel.infrastructure.rels.isDestination import isDestination
from metamodel.infrastructure.rels.isSource import isSource
from metamodel.organization.entities.Asset import Asset
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.rels.followedBy import followedBy
from metamodel.validation.semanticValidator import validateSemantics

PAPER_ENTITIES = {
    "Organization", "BusinessRequirement", "Sector", "HomeCountry", "InternationalBody",
    "AssetSecurityRequirement", "SecurityRequirement", "Infrastructure", "Node", "NodeType", "Connection",
    "Port", "Resource", "Asset", "Data", "DataType", "Code", "ApplicationInstance", "Application",
    "OSInstance", "OS", "User", "UserType", "Account", "PrivilegeLevel", "SecurityControl",
    "SecurityControlType", "ThreatActor", "Adversary", "AdversaryType", "Expertise", "Threat", "Campaign",
    "ThreatStep", "TTP", "AttackTool", "AttackToolInstance", "AttackToolConfiguration", "Indicator",
    "Vulnerability", "SoftwareVulnerability", "ConfigVulnerability", "HumanVulnerability",
}


@pytest.fixture(scope="module")
def registry():
    return Registry.load_default()


def test_entities_match_paper(registry):
    assert {c.__name__ for c in registry.get_entity_classes()} == PAPER_ENTITIES


def test_relationship_count(registry):
    assert len(registry.get_relationship_classes()) == 65


def test_every_entity_has_a_knowledge_class(registry):
    assert {c.knowledge_class for c in registry.get_entity_classes()} == {"concept", "system", "posteriori"}


@pytest.mark.parametrize("child, parent", [
    (Code, Resource), (Data, Resource), (Asset, Resource), (ApplicationInstance, Code),
])
def test_generalizations(child, parent):
    assert issubclass(child, parent)


@pytest.mark.parametrize("source, label, target, expected, src_card, tgt_card", [
    ("Node", "runsOS", "OSInstance", "runsOS", "1", "0..1"),
    ("ApplicationInstance", "uses", "Port", "uses", "0..1", "0..*"),
    ("User", "hasAccount", "Account", "hasAccount", "1", "0..*"),
    ("Account", "grantsAccessTo", "Node", "grantsAccessToNode", "0..*", "0..*"),
    ("Account", "grantsAccessTo", "Data", "grantsAccessToResource", "0..*", "1..*"),
    ("ConfigVulnerability", "affects", "Account", "affectsAccount", "0..*", "0..*"),
    ("SecurityControl", "protects", "Account", "protectsAccount", "0..*", "0..*"),
    ("SecurityControlType", "counters", "TTP", "counters", "0..*", "0..*"),
    ("Campaign", "focusesOn", "Sector", "targetsSector", "0..*", "0..*"),
    ("Threat", "partOf", "Campaign", "threatPartOf", "1..*", "0..1"),
    ("Adversary", "hasAdversaryType", "AdversaryType", "hasAdversaryType", "0..*", "1..*"),
])
def test_relationships_and_multiplicities(registry, source, label, target, expected, src_card, tgt_card):
    name = registry.resolve_relationship_alias(source, label, target)
    cls = registry.get_relationship_class(name)
    assert name == expected
    assert (cls.source_cardinality, cls.target_cardinality) == (src_card, tgt_card)


@pytest.mark.parametrize("name", ["hasAccessTo", "accessesInformation", "userAccessesInformation", "launches",
                                  "resourceImplementsCode", "applicationImplementsCode", "resourceImplementsAsset",
                                  "designedFor", "deployedTo"])
def test_removed_relationships(registry, name):
    assert not registry.has_relationship_type(name)


def test_legacy_names(registry):
    assert registry.canonical_entity_type("Information") == "Data"
    assert registry.resolve_relationship_type("listensOn") == "uses"
    assert registry.resolve_relationship_type("hasInformationType") == "hasDataType"


def test_privilege_level_association_class():
    model = Model()
    account = model.add(Account(name="admin@srv1", kind="domain"))
    node = model.add(Node(name="srv1"))
    admin = PrivilegeLevel(name="Administrator", rank=2)
    with pytest.raises(ValueError):
        model.add(grantsAccessToNode(account, node, privilege_level=admin))  # level not in the model
    model.add(admin)
    rel = model.add(grantsAccessToNode(account, node, privilege_level=admin))
    assert rel.get_attribute("privilege_level") is admin
    assert rel.to_dict()["privilege_level"] == admin.id
    with pytest.raises(ValueError):
        model.remove(admin)
    with pytest.raises(TypeError):
        grantsAccessToNode(account, node, privilege_level=node)
    with pytest.raises(TypeError):
        grantsAccessToNode(account, node, level=admin)


@pytest.mark.parametrize("kwargs", [dict(scope="dmz"), dict(scope=1)])
def test_connection_scope_values(kwargs):
    with pytest.raises((ValueError, TypeError)):
        Connection(name="c", **kwargs)


def test_threat_step_join_default_and_values():
    assert ThreatStep(name="s").join == "AND"
    assert ThreatStep(name="s", join="OR").join == "OR"
    with pytest.raises(ValueError):
        ThreatStep(name="s", join="XOR")


def test_account_kind_values():
    assert Account(name="a", kind="cloud").kind == "cloud"
    with pytest.raises(ValueError):
        Account(name="a", kind="root")


def test_semantics_connection_scope_and_cycles():
    model = Model()
    a, b = model.add(Node(name="a")), model.add(Node(name="b"))
    inbound = model.add(Connection(name="in", scope="inbound"))
    model.add(isSource(a, inbound))
    model.add(isDestination(b, inbound))
    s1, s2 = model.add(ThreatStep(name="s1")), model.add(ThreatStep(name="s2"))
    model.add(followedBy(s1, s2))
    model.add(followedBy(s2, s1))
    messages = [m.message for m in validateSemantics(model).errors]
    assert any("scope 'inbound' has 1 source" in m for m in messages)
    assert any("cycle" in m for m in messages)


def test_motivating_example_is_valid(motivating_model):
    report = motivating_model.validate()
    assert report.is_valid, report.errors
    assert report.warnings == []
