"""STIX parser example."""

from pathlib import Path

from metamodel.io.stixParser import loadStixBundle

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "bundle.json"
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    model = loadStixBundle(DATA_FILE)

    OUTPUT_DIR.mkdir(exist_ok=True)
    summary_file = OUTPUT_DIR / "stix_summary.txt"
    summary_file.write_text(
        f"Loaded entities: {len(model.entities)}\nLoaded relationships: {len(model.relationships)}\n",
        encoding="utf-8",
    )

    print(summary_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
