import pytest

from metamodel.core.Model import Model

from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Indicator import Indicator
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability
from metamodel.cyberThreat.entities.HumanVulnerability import HumanVulnerability
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.aliasOf import aliasOf
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.io.jsonParser import parseScenario


# AttackTool tests


def test_attack_tool_list_getters_return_copies():
    tool = AttackTool(
        name="Example tool",
        aliases=["ToolX"],
        capabilities=["Scanning"],
    )
    tool.aliases.append("Another alias")
    tool.capabilities.append("Exploitation")
    assert tool.aliases == ["ToolX"]
    assert tool.capabilities == ["Scanning"]


# AttackToolConfiguration tests


def test_attack_tool_configuration_parameters_getter_returns_copy():
    configuration = AttackToolConfiguration(
        name="Example configuration",
        parameters={"timeout": 30},
    )
    configuration.parameters["timeout"] = 60
    assert configuration.parameters == {"timeout": 30}


#AttackToolInstance


def test_attack_tool_instance_hashes_getter_returns_copy():
    instance = AttackToolInstance(name="Malware sample", hashes=["abc123"])
    instance.hashes.append("def456")
    assert instance.hashes == ["abc123"]


@pytest.mark.parametrize(
    "field, invalid_date",
    [
        ("first_seen", "2026-12-01"),
        ("last_seen", "2025-12-01"),
    ],
)
def test_attack_tool_instance_rejects_inverted_dates(field, invalid_date):
    instance = AttackToolInstance(
        name="Malware sample",
        first_seen="2026-01-10",
        last_seen="2026-10-30",
    )
    with pytest.raises(ValueError):
        setattr(instance, field, invalid_date)
    assert instance.first_seen == "2026-01-10"
    assert instance.last_seen == "2026-10-30"


def test_attack_tool_instance_rejects_inverted_dates_at_creation():
    with pytest.raises(ValueError):
        AttackToolInstance(
            name="Malware sample",
            first_seen="2026-10-30",
            last_seen="2026-01-10",
        )


# Indicator tests


def test_indicator_rejects_inverted_validity_dates():
    with pytest.raises(ValueError):
        Indicator(
            name="Example indicator",
            valid_from="2026-12-01",
            valid_until="2026-01-01",
        )
    indicator = Indicator(
        name="Example indicator",
        valid_from="2026-01-01",
        valid_until="2026-10-01",
    )
    with pytest.raises(ValueError):
        indicator.valid_until = "2025-12-01"
    assert indicator.valid_from == "2026-01-01"
    assert indicator.valid_until == "2026-10-01"


# SoftwareVulnerability tests


def test_software_vulnerability_affected_versions_getter_returns_copy():
    vulnerability = SoftwareVulnerability(
        name="Example vulnerability",
        affected_versions=["1.0", "1.1"],
    )
    vulnerability.affected_versions.append("2.0")
    assert vulnerability.affected_versions == ["1.0", "1.1"]


# Threat tests


def test_threat_rejects_inverted_dates_at_creation():
    with pytest.raises(ValueError):
        Threat(
            name="Example threat",
            first_seen="2026-10-30",
            last_seen="2026-01-10",
        )


def test_threat_rejects_invalid_first_seen_assignment():
    threat = Threat(
        name="Example threat",
        first_seen="2026-01-10",
        last_seen="2026-10-30",
    )
    with pytest.raises(ValueError):
        threat.first_seen = "2026-12-01"
    assert threat.first_seen == "2026-01-10"
    assert threat.last_seen == "2026-10-30"


def test_threat_rejects_invalid_last_seen_assignment():
    threat = Threat(
        name="Example threat",
        first_seen="2026-01-10",
        last_seen="2026-10-30",
    )
    with pytest.raises(ValueError):
        threat.last_seen = "2025-12-01"
    assert threat.first_seen == "2026-01-10"
    assert threat.last_seen == "2026-10-30"


@pytest.mark.parametrize(
    ("first_seen", "last_seen"),
    [
        ("2026-01-10", "2026-10-30"),
        ("2026-10-30", "2026-10-30"),
        ("2026-01-10", None),
        (None, "2026-10-30"),
        (None, None),
    ],
)
def test_threat_accepts_valid_date_combinations(first_seen, last_seen):
    threat = Threat(
        name="Example threat",
        first_seen=first_seen,
        last_seen=last_seen,
    )
    assert threat.first_seen == first_seen
    assert threat.last_seen == last_seen


# ThreatStep tests


def test_threat_step_condition_getters_return_copies():
    step = ThreatStep(
        name="Initial access",
        preconditions=["Service reachable"],
        postconditions=["Access obtained"],
    )

    step.preconditions.append(123)
    step.postconditions.append(123)
    assert step.preconditions == ["Service reachable"]
    assert step.postconditions == ["Access obtained"]


# ThreatActor tests


def test_threat_actor_aliases_getter_returns_copy():
    actor = ThreatActor(
        name="Example actor",
        aliases=["Group Alpha"],
    )
    actor.aliases.append(123)
    assert actor.aliases == ["Group Alpha"]


# Campaign tests


def test_campaign_rejects_inverted_dates_at_creation():
    with pytest.raises(ValueError):
        Campaign(
            name="Example campaign",
            first_seen="2026-10-30",
            last_seen="2026-01-10",
        )


def test_campaign_rejects_invalid_first_seen_assignment():
    campaign = Campaign(
        name="Example campaign",
        first_seen="2026-01-10",
        last_seen="2026-10-30",
    )

    with pytest.raises(ValueError):
        campaign.first_seen = "2026-12-01"
    assert campaign.first_seen == "2026-01-10"
    assert campaign.last_seen == "2026-10-30"


def test_campaign_rejects_invalid_last_seen_assignment():
    campaign = Campaign(
        name="Example campaign",
        first_seen="2026-01-10",
        last_seen="2026-10-30",
    )

    with pytest.raises(ValueError):
        campaign.last_seen = "2025-12-01"
    assert campaign.first_seen == "2026-01-10"
    assert campaign.last_seen == "2026-10-30"


@pytest.mark.parametrize(
    ("first_seen", "last_seen"),
    [
        ("2026-01-10", "2026-10-30"),
        ("2026-10-30", "2026-10-30"),
        ("2026-01-10", None),
        (None, "2026-10-30"),
        (None, None),
    ],
)
def test_campaign_accepts_valid_date_combinations(first_seen, last_seen):
    campaign = Campaign(
        name="Example campaign",
        first_seen=first_seen,
        last_seen=last_seen,
    )
    assert campaign.first_seen == first_seen
    assert campaign.last_seen == last_seen


# Vulnerability inheritance tests


@pytest.mark.parametrize(
    "cls,kwargs",
    [
        (SoftwareVulnerability, {"cve_id": "CVE-2099-1234", "cvss_score": 8.8}),
        (ConfigVulnerability, {"misconfiguration_type": "Missing MFA", "severity": "High"}),
        (HumanVulnerability, {"vulnerability_type": "Social Engineering", "severity": "High"}),
    ],
)
def test_vulnerability_subclasses_inherit_and_serialize(cls, kwargs):
    vuln = cls(name="Example", source="Synthetic", **kwargs)
    assert isinstance(vuln, Vulnerability)
    assert vuln.type == cls.__name__
    assert vuln.to_dict()["severity"] == getattr(vuln, "severity")
    assert vuln.to_dict()["cvss_score"] == getattr(vuln, "cvss_score")
    for key, value in kwargs.items():
        assert vuln.to_dict()[key] == value


def test_inherited_cvss_validation():
    with pytest.raises(ValueError):
        SoftwareVulnerability(name="Example", cvss_score=11.0)


def test_exploits_accepts_human_vulnerability():
    model = Model()
    step = model.add(ThreatStep(name="Credential Capture"))
    vulnerability = model.add(
        HumanVulnerability(
            name="Phishing Susceptibility",
            vulnerability_type="Social Engineering",
            severity="High",
        )
    )
    model.add(exploits(step, vulnerability))
    assert model.validate().is_valid


def test_factory_parse_scenario_preserves_inherited_fields():
    data = {
        "entities": [
            {
                "id": "v",
                "type": "HumanVulnerability",
                "name": "Human",
                "severity": "High",
                "vulnerability_type": "Social Engineering",
                "external_id": None,
                "cvss_score": None,
            },
            {
                "id": "s",
                "type": "ThreatStep",
                "name": "Credential Capture",
            },
        ],
        "relationships": [
            {
                "type": "exploits",
                "source": "s",
                "target": "v",
            }
        ],
    }
    model = parseScenario(data)
    assert model.validate().is_valid
    assert (
        model.get_entities_by_type("HumanVulnerability")[0]
        .to_dict()["severity"]
        == "High"
    )


# initiates tests


def test_initiates_allows_actor_alias_without_threat():
    model = Model()
    actor = model.add(ThreatActor(name="Silent Horizon Group"))
    alias = model.add(ThreatActor(name="Ghost Meridian"))
    threat = model.add(Threat(name="Research Espionage"))

    model.add(aliasOf(alias, actor))
    model.add(initiates(actor, threat))

    assert model.validate().is_valid


def test_initiates_rejects_multiple_threats_per_actor():
    model = Model()
    actor = model.add(ThreatActor(name="Silent Horizon Group"))
    threat1 = model.add(Threat(name="Credential Theft"))
    threat2 = model.add(Threat(name="Research Data Theft"))

    model.add(initiates(actor, threat1))
    model.add(initiates(actor, threat2))

    report = model.validate()

    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "cardinalityValidator"
    assert "initiates:" in report.errors[0].message
    assert "expected 0..1" in report.errors[0].message


def test_initiates_rejects_multiple_actors_for_same_threat():
    model = Model()
    actor1 = model.add(ThreatActor(name="Threat Actor 1"))
    actor2 = model.add(ThreatActor(name="Threat Actor 2"))
    threat = model.add(Threat(name="Research Espionage"))

    model.add(initiates(actor1, threat))
    model.add(initiates(actor2, threat))

    report = model.validate()

    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "cardinalityValidator"
    assert "initiates:" in report.errors[0].message