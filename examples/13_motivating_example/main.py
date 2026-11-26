"""Motivating example of the paper: variants A and B, validation, and export to every format."""

from pathlib import Path

from metamodel.infrastructure.entities.SecurityControl import SecurityControl
from metamodel.infrastructure.entities.SecurityControlType import SecurityControlType
from metamodel.infrastructure.rels.counters import counters
from metamodel.infrastructure.rels.protectsAccount import protectsAccount
from metamodel.infrastructure.rels.securityControlInstanceOf import securityControlInstanceOf
from metamodel.io import loadModel, saveModel

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def variant_b(model):
    """Variant B: phishing-resistant MFA protects the mailbox account and counters T1539."""
    mfa_type = model.add(SecurityControlType(name="Phishing-resistant MFA", catalogue="NIST SP 800-63B-4"))
    mfa = model.add(SecurityControl(name="FIDO2 MFA on mailbox accounts", status="enforced"))
    model.add(securityControlInstanceOf(mfa, mfa_type))
    model.add(protectsAccount(mfa, model.get_entity("mailbox-account")))
    model.add(counters(mfa_type, model.get_entity("t1539")))
    model.metadata["name"] = "Motivating example - variant B"
    return model


def main() -> None:
    model = loadModel(BASE_DIR / "data" / "scenario.yaml")
    report = model.validate()
    print(f"Variant A: {len(model.entities)} entities, {len(model.relationships)} relationships, valid: {report.is_valid}")

    model_b = variant_b(loadModel(BASE_DIR / "data" / "scenario.yaml"))
    print(f"Variant B: valid: {model_b.validate().is_valid}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    for name in ("variant_b.json", "variant_b.yaml", "variant_b.graphml", "variant_b.cypher", "variant_b_csv"):
        saveModel(model_b, OUTPUT_DIR / name, "csv" if name.endswith("_csv") else None)
        print("wrote", OUTPUT_DIR / name)


if __name__ == "__main__":
    main()
