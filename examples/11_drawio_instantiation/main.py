"""draw.io instantiation example."""

from pathlib import Path

from metamodel.io.drawioParser import loadDrawioScenario

BASE_DIR = Path(__file__).resolve().parent
DRAWIO_FILE = BASE_DIR / "data" / "scenario.drawio.xml"


def main() -> None:
    model = loadDrawioScenario(DRAWIO_FILE)
    print(f"Loaded entities: {len(model.entities)}")
    print(f"Loaded relationships: {len(model.relationships)}")


if __name__ == "__main__":
    main()
