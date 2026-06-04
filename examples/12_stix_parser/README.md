# Example 12: STIX parser

This example parses a STIX 2.1 bundle and instantiates CTI Feasibility Metamodel entities and relationships.

The parser accepts all STIX Domain Objects and STIX Relationship Objects listed in the official STIX introduction. Native mappings are used where the CTI Feasibility Metamodel has a clear counterpart; otherwise, STIX objects are preserved as `GenericStixObject` instances.

## Native mappings

| STIX type | Native metamodel entity |
|---|---|
| `attack-pattern` | `TTP` |
| `campaign` | `Campaign` |
| `indicator` | `Indicator` |
| `intrusion-set` | `Adversary` |
| `malware` | `AttackTool` |
| `threat-actor` | `ThreatActor` |
| `tool` | `AttackTool` |
| `vulnerability` | `Vulnerability` |

All other official STIX object types are preserved as `GenericStixObject`.

STIX `relationship` and `sighting` SROs are preserved as `GenericStixRelationship` where their referenced endpoints are available.

## Run

From the repository root:

```bash
python examples/12_stix_parser/main.py
```

## Input

```text
data/bundle.json
```

## Extensibility

You can register additional object mappers:

```python
from metamodel.io.stixParser import StixParser

parser = StixParser()
parser.register_object_mapper("course-of-action", my_course_of_action_mapper)
```

You can register additional relationship mappers:

```python
parser.register_relationship_mapper("sighting", my_sighting_mapper)
```
