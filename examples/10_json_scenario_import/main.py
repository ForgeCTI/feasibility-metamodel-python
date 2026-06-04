"""JSON scenario import example."""

from pathlib import Path

from metamodel.io.jsonParser import loadJsonScenario

BASE_DIR = Path(__file__).resolve().parent
SCENARIO_FILE = BASE_DIR / "data" / "scenario.json"


def main() -> None:
    model = loadJsonScenario(SCENARIO_FILE)
    print(f"Loaded entities: {len(model.entities)}")
    print(f"Loaded relationships: {len(model.relationships)}")
    print(f"Valid: {model.validate().is_valid}")


if __name__ == "__main__":
    main()
