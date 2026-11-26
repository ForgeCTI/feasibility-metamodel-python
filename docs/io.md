# I/O

The `io` package reads and writes scenario files; `adapters` convert models to and from external graph
libraries and databases (see [Adapters](adapters.md)).

```text
src/metamodel/io/
├── serialization.py   model <-> scenario data (shared by every format)
├── jsonParser.py / jsonSerializer.py
├── yamlParser.py / yamlSerializer.py
├── csvParser.py / csvSerializer.py
├── formats.py         loadModel / saveModel by format or extension
├── drawioParser.py    draw.io diagrams (import)
└── stixParser.py      STIX 2.1 bundles (import), see stix/
```

## Scenario format

```yaml
metadata:                      # optional, preserved by every format
  name: Motivating example - variant A
  completeness: [Node, Account, Connection]
entities:
  - {id: mx, type: Node, name: Mail server, hostname: mx1}
  - {id: acc, type: Account, name: Mailbox account, kind: cloud}
  - {id: std, type: PrivilegeLevel, name: Standard user, rank: 1}
relationships:
  - {type: grantsAccessTo, source: acc, target: mx, privilege_level: std}
```

* `id` values are kept as entity and relationship ids, so a model can be exported and re-imported
  without changing them; missing ids are generated.
* A relationship `type` can be the class name (`grantsAccessToNode`), the metamodel label
  (`grantsAccessTo`, resolved from the endpoint types along the class hierarchy), or a legacy name
  (`listensOn` → `uses`, `hasInformationType` → `hasDataType`). Legacy entity types `Information`
  and `InformationType` are read as `Data` and `DataType`.
* Relationship attributes are written next to `source` and `target`; entity-valued attributes
  (`privilege_level`) hold entity ids.
* Parsing is strict by default: unknown types, unknown attributes, or invalid values raise
  `ParseError` naming the entity. Use `strict=False` (or `parseScenarioWithReport`) to skip them and
  collect warnings.

## Python API

```python
from metamodel.io import loadModel, saveModel, parseScenario, model_to_data

model = loadModel("scenario.yaml")          # format from the extension; a directory is CSV
saveModel(model, "scenario.json")
saveModel(model, "scenario_csv", "csv")
saveModel(model, "load.cypher")
data = model_to_data(model, include_none=False)
model = parseScenario(data)
```

Format-specific functions remain available: `loadJsonScenario`, `saveJsonScenario`, `loadYamlScenario`,
`saveYamlScenario`, `loadCsvScenario(entities_csv, relationships_csv)`, `loadCsvDirectory(dir)`,
`saveCsvScenario`, `saveCsvDirectory`, and the string variants `loadsJsonScenario`, `dumpsJsonScenario`,
`loadsYamlScenario`, `dumpsYamlScenario`.

## CSV

A CSV scenario is a directory with:

* `entities.csv`: `id,type,name,description,source` followed by one column per attribute used;
* `relationships.csv`: `id,type,source,target` followed by one column per relationship attribute;
* `metadata.json` (optional).

Empty cells mean "not set". Cells are converted to the attribute types: `true`/`false`, integers and
floats, lists written as JSON (`["10.0.0.1","10.0.0.2"]`) or separated by `;`, and dicts as JSON.

## STIX and draw.io

`loadStixBundle(path)` and `loadStixBundleWithReport(path)` map STIX 2.1 objects to entities (see
`io/stix/`); `loadDrawioScenario(path)` instantiates entities whose labels are entity types and edges
whose labels are relationship labels.
