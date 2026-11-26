# Taxonomies

Taxonomies hold reusable controlled vocabularies (attack tools, ATT&CK techniques, weaknesses,
platforms, node, user, and data types, sectors, countries, security requirements), kept separate from
the instances of a scenario.

| Layer | Meaning | Example |
|---|---|---|
| Taxonomy concept | Reusable reference knowledge | `attackTools:cobaltStrike` |
| Metamodel entity | Entity type defined by the metamodel | `AttackTool` |
| Scenario instance | Concrete object in a model | `AttackTool(name="Cobalt Strike")` |

Taxonomy concepts are used to create entities with consistent names and attributes; identifiers from
external catalogues are kept in entity attributes such as `TTP.external_id` or
`Vulnerability.external_id`. Entities do not store a taxonomy reference (the former `taxonomy_ref`
attribute was removed), and the model validators do not check taxonomies.

Many generic entities correspond to the a-priori, generic knowledge class of the paper
(`knowledge_class == "concept"`): `TTP`, `AttackTool`, `Sector`, `HomeCountry`, `NodeType`,
`UserType`, `DataType`, `OS`, `Application`, `SecurityControlType`, and others. These are the natural
candidates for taxonomy-backed instantiation.

## Reference format

Concepts are addressed as `<taxonomy>:<concept>`:

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1059
cwe:CWE-79
sectors:finance
nodeTypes:webServer
userTypes:administrator
dataTypes:credentials
securityRequirements:confidentiality
```

The part before `:` is the taxonomy id, the part after it the concept id. Lookup also accepts a
concept name or alias (case-insensitive) in place of the id.

## Bundled taxonomies

```text
src/metamodel/taxonomies/
├── Taxonomy.py, TaxonomyConcept.py, TaxonomyMapping.py, TaxonomyRegistry.py
├── attackTools/       attackTools.yaml
├── ttps/              mitreAttackEnterprise.yaml
├── vulnerabilities/   cwe.yaml, capec.yaml
├── platforms/         operatingSystems.yaml, applications.yaml, cloudServices.yaml
├── infrastructure/    nodeTypes.yaml, userTypes.yaml, dataTypes.yaml, portTypes.yaml
└── organization/      sectors.yaml, countries.yaml, internationalBodies.yaml, securityRequirements.yaml
```

The bundled files are small, illustrative vocabularies (e.g. a few ATT&CK techniques), not complete
copies of the external catalogues. Loading them requires the `[yaml]` extra.

## Taxonomy files

```yaml
taxonomy:
  id: attackTools
  version: "0.1"
  source: Project-maintained taxonomy
  concepts:
    - id: cobaltStrike
      name: Cobalt Strike
      category: command_and_control
      description: Commercial adversary simulation framework frequently abused by threat actors.
      aliases: [Beacon]
      external_references:
        - {source: MITRE ATT&CK Software, external_id: S0154}
      tags: []
      properties: {}
```

| Field | Required | Meaning |
|---|---:|---|
| `id` | yes | Stable concept identifier within the taxonomy |
| `name` | no (defaults to `id`) | Human-readable name |
| `description` | no | Text description |
| `category` | no | Category or family |
| `aliases` | no | Alternative names, used by lookup |
| `external_references` | no | References to external catalogues |
| `tags` | no | Labels for filtering |
| `properties` | no | Taxonomy-specific fields |

## Looking up concepts

```python
from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry

taxonomies = TaxonomyRegistry.load_default()      # all bundled files
print(sorted(taxonomies.taxonomies))

tool = taxonomies.resolve("attackTools:cobaltStrike")
print(tool.name, tool.aliases, tool.external_references)

assert taxonomies.resolve("attackTools:Beacon") is tool   # alias lookup
assert not taxonomies.contains("attackTools:unknownTool")
```

`resolve` returns `None` for malformed or unknown references, and `contains` returns whether a
reference resolves. Additional taxonomies can be registered with
`taxonomies.register(Taxonomy.from_dict(data))`.

## Creating entities from concepts

```python
from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.TTP import TTP

model = Model()

concept = taxonomies.resolve("attackTools:cobaltStrike")
cobalt_strike = model.add(AttackTool(
    name=concept.name,
    description=concept.description,
    aliases=concept.aliases,
    tool_type=concept.category,
    source="attackTools:cobaltStrike",               # provenance of the instance
))

technique = taxonomies.resolve("mitreAttackEnterprise:T1059")
ttp = model.add(TTP(name=technique.name, external_id=technique.id))
```

The generic concept and the concrete observation remain distinct entities linked by the metamodel:

```python
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf

beacon = model.add(AttackToolInstance(name="Beacon observed in case study 1", observed_version="4.9"))
model.add(toolInstanceOf(beacon, cobalt_strike))
```

The same concept can thus be reused across many scenarios, while each scenario records its own
instances (an a-posteriori observation, here).

## Taxonomies and STIX

The STIX parser maps STIX objects to native entities where a clear correspondence exists
(`attack-pattern` to `TTP`, `tool` and `malware` to `AttackTool`, `vulnerability` to
`Vulnerability`, ...). External references of STIX objects (e.g. `mitre-attack`/`T1059`) are kept in
the entity's `external_id`, which can be looked up in a taxonomy when one is available.

## Mappings and versioning

`TaxonomyMapping(entity_type, taxonomy_id)` records which taxonomy provides the concepts of an
entity type (e.g. `AttackTool` → `attackTools`). Taxonomies carry a `version`; keep concept ids stable
once published, mark superseded concepts instead of deleting them, and record the version used by a case study for reproducibility.

## Recommended design

Prefer stable ids, concise names, explicit categories, aliases for CTI naming variation, external
references, and version metadata. Avoid using descriptions as ids, mixing scenario-specific
observations with reusable concepts, and encoding in a taxonomy relationships that belong to the
metamodel.
