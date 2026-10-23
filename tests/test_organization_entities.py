import pytest

from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.Organization import Organization

# Sector tests


def test_sector_code_requires_standard():
    with pytest.raises(ValueError):
        Sector(name="Finance", sector_code="K")


def test_sector_standard_version_requires_standard():
    with pytest.raises(ValueError):
        Sector(name="Finance", sector_standard_version="Rev. 2.1")


def test_sector_standard_cannot_be_removed_when_dependent_fields_exist():
    sector = Sector(
        name="Finance", 
        sector_standard="NACE", 
        sector_code="K", 
        sector_standard_version="Rev. 2.1",
    )
    with pytest.raises(ValueError):
        sector.sector_standard = None


def test_sector_standard_version_is_serialized():
    sector = Sector(
        name="Finance",
        sector_standard="NACE",
        sector_standard_version="Rev. 2.1",
    )
    data = sector.to_dict()
    assert data["sector_standard_version"] == "Rev. 2.1"


# HomeCountry tests


def test_home_country_accepts_valid_iso_codes():
    country = HomeCountry(
        name="Italy",
        iso2_code="IT",
        iso3_code="ITA",
    )
    assert country.iso2_code == "IT"
    assert country.iso3_code == "ITA"


def test_home_country_rejects_lowercase_iso_codes():
    with pytest.raises(ValueError):
        HomeCountry(
            name="Italy",
            iso2_code="it",
        )


def test_home_country_rejects_invalid_iso_code_length():
    with pytest.raises(ValueError):
        HomeCountry(
            name="Italy",
            iso3_code="IT",
        )


def test_home_country_rejects_non_alphabetic_iso_codes():
    with pytest.raises(ValueError):
        HomeCountry(
            name="Italy",
            iso2_code="I1",
        )


# SecurityRequirement tests


def test_security_requirement_family_requires_framework():
    with pytest.raises(ValueError):
        SecurityRequirement(
            name="Access restriction",
            control_family="Access Control",
        )


def test_security_requirement_accepts_framework_and_family():
    requirement = SecurityRequirement(
        name="Access restriction",
        control_framework="NIST SP 800-53",
        control_family="Access Control",
    )
    assert requirement.control_framework == "NIST SP 800-53"
    assert requirement.control_family == "Access Control"


def test_security_requirement_framework_cannot_be_removed_with_family():
    requirement = SecurityRequirement(
        name="Access restriction",
        control_framework="NIST SP 800-53",
        control_family="Access Control",
    )
    with pytest.raises(ValueError):
        requirement.control_framework = None


# Organization tests


def test_organization_rejects_invalid_website():
    with pytest.raises(ValueError):
        Organization(
            name="Example Organization",
            website="not-a-url",
        )


def test_organization_accepts_valid_website():
    organization = Organization(
        name="Example Organization",
        website="https://example.com",
    )

    assert organization.website == "https://example.com"

