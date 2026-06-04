import pytest

from metamodel.cyberThreat.entities.Vulnerability import Vulnerability


def test_cvss_range():
    with pytest.raises(ValueError):
        Vulnerability(name="bad", cvss_score=11.0)
