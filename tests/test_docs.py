"""Run the Python code blocks of the documentation pages that are meant to be executable.

Blocks of one page share a namespace and run in order. A block preceded by the line
``<!-- no-test -->`` is skipped (e.g. examples that need a Neo4j server or show an error).
"""
import re
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parents[1] / "docs"
PAGES = ["quickstart.md", "index.md", "validation.md", "metamodel.md", "taxonomies.md", "io.md", "adapters.md"]
BLOCK = re.compile(r"(<!-- no-test -->\s*\n)?```python\n(.*?)```", re.S)


@pytest.mark.parametrize("page", PAGES)
def test_python_blocks_run(page, monkeypatch, tmp_path):
    pytest.importorskip("yaml")
    pytest.importorskip("networkx")
    # Run in an empty directory (examples write files) that can still reach examples/.
    (tmp_path / "examples").symlink_to(Path(__file__).resolve().parents[1] / "examples", target_is_directory=True)
    monkeypatch.chdir(tmp_path)
    namespace: dict = {"__name__": "__docs__"}
    for index, (skip, code) in enumerate(BLOCK.findall((DOCS / page).read_text(encoding="utf-8"))):
        if skip:
            continue
        try:
            exec(compile(code, f"{page}[block {index}]", "exec"), namespace)
        except Exception as exc:  # pragma: no cover - reported by pytest
            pytest.fail(f"{page}, block {index}: {type(exc).__name__}: {exc}")
