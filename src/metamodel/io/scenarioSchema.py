SCENARIO_SCHEMA_DESCRIPTION = {
    "metadata": "Optional mapping of scenario metadata (e.g. name, description, completeness set).",
    "entities": "List of entity dictionaries. Each item requires type and name; id is preserved and referenced by relationships.",
    "relationships": "List of relationship dictionaries. Each item requires type (class name or metamodel label), source, and target; "
                     "relationship attributes (e.g. privilege_level for grantsAccessTo) hold values or entity ids.",
}
