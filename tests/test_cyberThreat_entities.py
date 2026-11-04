import pytest

from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Campaign import Campaign


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
