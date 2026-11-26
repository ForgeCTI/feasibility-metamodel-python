# Motivating example

The motivating example of the paper (Section 2.2): Star Blizzard credential phishing
against a UK defence organization, with threat steps TS1 (T1566.001), TS2 (T1539), and
TS3 (T1114.002).

* `data/scenario.yaml` is variant A (no phishing-resistant MFA). It uses the new
  metamodel elements: `Account`, `PrivilegeLevel` on `grantsAccessTo`, `Connection.scope`,
  `ApplicationInstance --uses--> Port`, `Asset` as a `Resource`, and the separation
  between the CTI layer and a-posteriori (inferred) edges.
* `main.py` builds variant B by adding a `SecurityControl` that protects the mailbox
  account and whose type counters T1539, validates both, and exports variant B to JSON,
  YAML, GraphML, Cypher, and CSV.

```bash
pip install -e ".[yaml,networkx]"
python examples/13_motivating_example/main.py
metamodel validate examples/13_motivating_example/data/scenario.yaml
metamodel inspect examples/13_motivating_example/data/scenario.yaml
```
