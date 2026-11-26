// Illustration of the TS3 precondition of the paper (Table 2) on the motivating example:
// an account granting access to a resource hosted on a node reachable through an
// inbound connection, with a privilege level at least the one required by the resource.
// Negative patterns (controls countering T1114.002 that protect a, r, or m) and the
// dependency on TS2 are left to the evaluation code.
MATCH (a:Account)-[g:grantsAccessTo]->(r:Resource)<-[:hostsResource]-(m:Node)-[:isDestination]->(k:Connection {scope: 'inbound'})
OPTIONAL MATCH (r)-[:requiresPrivilegeLevel]->(req:PrivilegeLevel)
WITH a, g, r, m, k, req
WHERE req IS NULL OR coalesce(g.privilege_level_rank, -1) >= req.rank
RETURN a.name AS account, r.name AS resource, m.name AS node, k.name AS connection;
