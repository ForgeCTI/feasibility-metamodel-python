MATCH (n)-[r]->(m)
RETURN labels(n) AS source_labels, n.name AS source_name, type(r) AS relationship, labels(m) AS target_labels, m.name AS target_name
LIMIT 50;
