import pytest

from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.InternationalBody import InternationalBody


# Sector tests


def test_sector_code_without_standard():
    sector = Sector(name="Finance", sector_code="K")

    assert sector.sector_code == "K"
    assert sector.sector_standard is None



def test_sector_standard_version_requires_standard():
    with pytest.raises(ValueError):
        Sector(name="Finance", sector_standard_version="Rev. 2.1")


def test_sector_standard_cannot_be_removed_when_version_exists():
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


@pytest.mark.parametrize(
    "requirement_type",
    ["confidentiality", "integrity", "availability"],
)
def test_security_requirement_valid_types(requirement_type):
    requirement = SecurityRequirement(
        name="Security requirement",
        requirement_type=requirement_type,
    )
    assert requirement.requirement_type == requirement_type


def test_security_requirement_invalid_type():
    with pytest.raises(ValueError):
        SecurityRequirement(
            name="Security requirement",
            requirement_type="authentication",
        )


def test_security_requirement_invalid_data_type():
    with pytest.raises(TypeError):
        SecurityRequirement(
            name="Security requirement",
            requirement_type=123,
        )


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


# InternationalBody tests


def test_international_body_valid_acronym():
    body = InternationalBody(
        name="European Union Agency for Cybersecurity",
        acronym="ENISA",
    )

    assert body.acronym == "ENISA"
    assert body.to_dict()["acronym"] == "ENISA"


@pytest.mark.parametrize("acronym", [None, "", "   ", 123])
def test_international_body_invalid_acronym(acronym):
    with pytest.raises((TypeError, ValueError)):
        InternationalBody(
            name="Example",
            acronym=acronym,
        )


def test_international_body_missing_acronym():
    with pytest.raises(TypeError):
        InternationalBody(name="Example")
