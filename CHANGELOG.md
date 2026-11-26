# Changelog

## 0.2.0

Metamodel aligned with the paper (43 entities, 65 relationships; see `docs/schema.md`).

### Added
- Entities `Account`, `PrivilegeLevel`, `SecurityControl`, `SecurityControlType`.
- Relationships `hasAccount`, `grantsAccessTo` (to `Node` and `Resource`, with the association class
  `PrivilegeLevel` as attribute `privilege_level`), `requiresPrivilegeLevel`, `instanceOf`
  (SecurityControl to SecurityControlType), `protects` (Node, User, Account, Resource), `mitigates`,
  `counters`, `uses` (ApplicationInstance to Port), `affects` (ConfigVulnerability to Account).
- Attributes `Connection.scope`, `ThreatStep.join`, `ApplicationInstance.role`, `OS.family`, and the
  class attribute `knowledge_class` on every entity.
- Relationship classes declare their metamodel `label`; relationships can carry attributes.
- Semantic validation: connection scopes, acyclic `followedBy`, ranks of privilege levels.
- I/O: id-preserving JSON/YAML/CSV import and export, scenario metadata, label and legacy-name
  resolution, strict and lenient parsing, `loadModel`/`saveModel`.
- Adapters: `fromNetworkx`, GraphML import, Neo4j import, batched parameterized Cypher, Cypher scripts.
- CLI: `convert -o` to every format, `schema`, `neo4j export|import`, JSON output, `--strict`, `--lenient`.
- Example 13 (motivating example of the paper, variants A and B); `scripts/build_registry.py`,
  `scripts/generate_schema_docs.py`.

### Changed
- `Information`/`InformationType` renamed `Data`/`DataType` (`hasInformationType` → `hasDataType`);
  old names are accepted by the importers.
- `Code`, `Data`, and `Asset` specialize `Resource`; `ApplicationInstance` and `OSInstance` specialize `Code`.
- Multiplicities follow the paper's figures (e.g. `runsOS` 0..1, `initiates` 1..*, `basedIn` 0..*/1..*).
  `startsWith` is 0..* at the Threat end (the figure's 1 would make every step a first step).
- Associations with several target types are validated on their union (e.g. a software vulnerability
  affects at least one OS or application); runsApp/runsOS count as hostsResource.

### Removed
- `hasAccessTo`, `accessesInformation`, `userAccessesInformation` (replaced by accounts and grants),
  `launches`, `listensOn` (replaced by `uses`), `resourceImplementsCode`, `applicationImplementsCode`,
  `resourceImplementsAsset` (replaced by generalizations), `designedFor`, `deployedTo` (not in the metamodel).

## 0.1.0

Initial generated implementation.
