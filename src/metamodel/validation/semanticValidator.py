"""Metamodel rules that multiplicities cannot express (see the paper, Sections 3.5 and 3.7)."""
from collections import defaultdict

from metamodel.core.ValidationReport import ValidationReport

_SCOPE_ENDPOINTS = {
    # scope: (number of isSource, number of isDestination)
    "internal": (1, 1),
    "inbound": (0, 1),
    "outbound": (1, 0),
}


def validateSemantics(model) -> ValidationReport:
    """Check connection scopes, acyclic threat-step ordering, and privilege levels.

    * a connection with scope ``internal`` has one source and one destination node,
      ``inbound`` only a destination, ``outbound`` only a source;
    * ``followedBy`` is acyclic, so threat steps can be evaluated in topological order;
    * a privilege level used by ``grantsAccessTo`` or ``requiresPrivilegeLevel``
      should have a ``rank``, otherwise grants cannot be compared (warning).
    """
    report = ValidationReport()
    sources, destinations = defaultdict(int), defaultdict(int)
    successors = defaultdict(list)
    used_levels = {}
    for rel in model.relationships:
        if rel.type == "isSource":
            sources[rel.target_entity.id] += 1
        elif rel.type == "isDestination":
            destinations[rel.target_entity.id] += 1
        elif rel.type == "followedBy":
            successors[rel.source_entity.id].append(rel.target_entity.id)
        elif rel.type == "requiresPrivilegeLevel":
            used_levels[rel.target_entity.id] = rel.target_entity
        for referenced in rel.referenced_entities():
            if referenced.type == "PrivilegeLevel":
                used_levels[referenced.id] = referenced

    for connection in model.get_entities_by_type("Connection"):
        scope = getattr(connection, "scope", None)
        if scope is None:
            report.add_warning("semanticValidator", f"Connection {connection.name!r} has no scope.")
            continue
        expected = _SCOPE_ENDPOINTS[scope]
        actual = (sources.get(connection.id, 0), destinations.get(connection.id, 0))
        if actual != expected:
            report.add_error(
                "semanticValidator",
                f"Connection {connection.name!r} with scope {scope!r} has {actual[0]} source and "
                f"{actual[1]} destination node(s); expected {expected[0]} and {expected[1]}.",
            )

    # cycle detection on followedBy (iterative DFS)
    state: dict[str, int] = {}
    for start in list(successors):
        if state.get(start):
            continue
        stack = [(start, iter(successors[start]))]
        state[start] = 1
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                state[node] = 2
                stack.pop()
            elif state.get(child) == 1:
                report.add_error("semanticValidator",
                                 f"followedBy contains a cycle through ThreatStep {model.get_entity(child).name!r}.")
                stack = []
                break
            elif not state.get(child):
                state[child] = 1
                stack.append((child, iter(successors.get(child, []))))
        if report.errors:
            break

    for level in used_levels.values():
        if getattr(level, "rank", None) is None:
            report.add_warning("semanticValidator", f"PrivilegeLevel {level.name!r} has no rank.")
    return report
