// Entities by type and knowledge class
MATCH (n:Entity) RETURN n.type AS type, n.knowledge_class AS knowledge_class, count(*) AS entities ORDER BY type;

// Relationships by metamodel label and class
MATCH (:Entity)-[r]->(:Entity) RETURN type(r) AS label, r.class AS class, count(*) AS relationships ORDER BY label;

// Supertype labels: every Resource, whatever its subtype
MATCH (r:Resource) RETURN r.type AS type, r.name AS name;
