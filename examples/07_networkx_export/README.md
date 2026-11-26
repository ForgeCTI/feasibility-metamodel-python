# NetworkX export

## Purpose

Convert the motivating example of the paper to a NetworkX `MultiDiGraph`, query it, and
round-trip it through NetworkX and GraphML.

## Run

From the repository root:

```bash
pip install -e ".[yaml,networkx]"
python examples/07_networkx_export/main.py
```

## Graph layout

* nodes are entities (key: entity id) with attributes `type`, `labels` (the type and its
  superclasses, e.g. `["ApplicationInstance", "Code", "Resource"]`), `knowledge_class`,
  `name`, and the domain attributes;
* edges are relationships (key: relationship id) with attributes `type` (class),
  `label` (metamodel label, e.g. `grantsAccessTo`), and relationship attributes
  (e.g. `privilege_level`, holding the id of a PrivilegeLevel entity).

`fromNetworkx` converts such a graph back to a model; GraphML stores lists and dicts as JSON strings.
