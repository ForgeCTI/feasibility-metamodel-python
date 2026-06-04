"""Cardinality validation example.

The exact error messages depend on the current cardinality rules implemented in the package.
"""

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization


def main() -> None:
    model = Model()

    # This organization is intentionally left without its expected contextual links.
    model.add_entity(Organization(name="Organization without sector"))

    report = model.validate()

    print(f"Valid: {report.is_valid}")
    print("Errors:")
    for error in report.errors:
        print(f"- {error}")


if __name__ == "__main__":
    main()
