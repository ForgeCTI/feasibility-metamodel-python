from pathlib import Path

root = Path(__file__).resolve().parents[1] / "src" / "metamodel"
for folder in root.glob("*/entities"):
    for path in folder.glob("*.py"):
        if path.name == "__init__.py":
            continue
        assert path.stem[0].isupper(), f"Entity file must start with a capital letter: {path}"
print("Naming checks passed.")
