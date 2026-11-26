import json

from metamodel.cli.main import main

from conftest import MOTIVATING


def test_validate(capsys):
    assert main(["validate", str(MOTIVATING)]) == 0
    assert "Valid: True" in capsys.readouterr().out


def test_validate_json_and_failure(tmp_path, capsys):
    broken = tmp_path / "s.json"
    broken.write_text(json.dumps({"entities": [{"id": "n", "type": "Node", "name": "n"}], "relationships": []}))
    assert main(["validate", str(broken), "--json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["valid"] is False and report["messages"]


def test_inspect(capsys):
    assert main(["inspect", str(MOTIVATING), "--json"]) == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["entities"] == 34 and summary["entity_types"]["ThreatStep"] == 3


def test_convert_to_files_and_back(tmp_path, capsys):
    for target in ("s.json", "s.yaml", "s.graphml", "csvdir"):
        assert main(["convert", str(MOTIVATING), "-o", str(tmp_path / target)] + (["--to", "csv"] if target == "csvdir" else [])) == 0
        assert main(["validate", str(tmp_path / target)]) == 0
    assert main(["convert", str(MOTIVATING), "-o", str(tmp_path / "s.cypher")]) == 0
    assert (tmp_path / "s.cypher").read_text().count("MERGE") > 30


def test_convert_to_stdout(capsys):
    assert main(["convert", str(MOTIVATING), "--to", "cypher"]) == 0
    assert "CREATE CONSTRAINT" in capsys.readouterr().out
    assert main(["convert", str(MOTIVATING), "--to", "csv"]) == 2


def test_schema(capsys):
    assert main(["schema", "--json"]) == 0
    schema = json.loads(capsys.readouterr().out)
    assert len(schema["entities"]) == 43 and len(schema["relationships"]) == 65
    assert main(["schema", "grantsAccessTo"]) == 0
    assert "privilege_level" in capsys.readouterr().out


def test_errors_are_reported(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "missing.json")]) == 2
    assert "error:" in capsys.readouterr().err


def test_neo4j_requires_password(monkeypatch, capsys):
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
    assert main(["neo4j", "export", str(MOTIVATING)]) == 2
    assert "password" in capsys.readouterr().err
