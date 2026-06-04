"""Default STIX mappers.

The mapper list is intentionally extensible. Native mappings are provided where
there is a clear CTI Feasibility Metamodel counterpart. All other official STIX
objects are preserved as GenericStixObject instances.
"""

from __future__ import annotations

from typing import Any
import re

from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Indicator import Indicator
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability

from metamodel.io.stix.constants import STIX_OBJECT_TYPES
from metamodel.io.stix.generic import GenericStixObject, GenericStixRelationship
from metamodel.io.stix.registry import (
    StixObjectMapperRegistry,
    StixRelationshipMapperRegistry,
)


def build_default_object_registry() -> StixObjectMapperRegistry:
    """Build the default object mapper registry."""
    registry = StixObjectMapperRegistry()

    for stix_type in STIX_OBJECT_TYPES:
        registry.register(stix_type, map_generic_object)

    registry.register("attack-pattern", map_attack_pattern)
    registry.register("campaign", map_campaign)
    registry.register("indicator", map_indicator)
    registry.register("intrusion-set", map_intrusion_set)
    registry.register("malware", map_malware)
    registry.register("threat-actor", map_threat_actor)
    registry.register("tool", map_tool)
    registry.register("vulnerability", map_vulnerability)

    return registry


def build_default_relationship_registry() -> StixRelationshipMapperRegistry:
    """Build the default relationship mapper registry."""
    registry = StixRelationshipMapperRegistry()
    registry.register("relationship", map_relationship)
    registry.register("sighting", map_sighting)
    return registry


def map_generic_object(obj: dict[str, Any], context) -> GenericStixObject:
    """Preserve any STIX object as a generic metamodel entity."""
    return GenericStixObject(
        stix_type=str(obj.get("type", "unknown")),
        stix_id=str(obj.get("id", "<missing-id>")),
        name=_name(obj),
        description=obj.get("description") if isinstance(obj.get("description"), str) else None,
        raw=obj,
        source=_source(obj),
    )


def map_threat_actor(obj: dict[str, Any], context) -> ThreatActor:
    return ThreatActor(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        aliases=_aliases(obj),
        motivation=_first_str(obj.get("primary_motivation")) or _first_str(obj.get("secondary_motivations")),
        sophistication=_map_sophistication(_first_str(obj.get("sophistication"))),
        country=None,
        taxonomy_ref=_taxonomy_ref(obj, "stixThreatActor"),
        source=_source(obj),
    )


def map_intrusion_set(obj: dict[str, Any], context) -> Adversary:
    return Adversary(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        objective=_first_str(obj.get("goals")),
        intent=None,
        capability_level=None,
        source=_source(obj),
    )


def map_campaign(obj: dict[str, Any], context) -> Campaign:
    return Campaign(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        first_seen=_date_only(obj.get("first_seen")),
        last_seen=_date_only(obj.get("last_seen")),
        status="unknown",
        objective=_first_str(obj.get("objective")) or _first_str(obj.get("labels")),
        source=_source(obj),
    )


def map_attack_pattern(obj: dict[str, Any], context) -> TTP:
    external_id = _external_id(obj)

    return TTP(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        taxonomy_ref=_taxonomy_ref(obj, "stixAttackPattern"),
        external_id=external_id,
        tactic=None,
        technique=external_id or _name(obj),
        subtechnique=None,
        source=_source(obj),
    )


def map_tool(obj: dict[str, Any], context) -> AttackTool:
    tool_types = obj.get("tool_types", [])

    return AttackTool(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        taxonomy_ref=_taxonomy_ref(obj, "stixTool"),
        aliases=_aliases(obj),
        tool_type=_map_tool_type(_first_str(tool_types)),
        capabilities=_as_str_list(tool_types),
        source=_source(obj),
    )


def map_malware(obj: dict[str, Any], context) -> AttackTool:
    malware_types = obj.get("malware_types", [])

    return AttackTool(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        taxonomy_ref=_taxonomy_ref(obj, "stixMalware"),
        aliases=_aliases(obj),
        tool_type="malware",
        capabilities=_as_str_list(malware_types),
        source=_source(obj),
    )


def map_indicator(obj: dict[str, Any], context) -> Indicator:
    pattern = obj.get("pattern")

    return Indicator(
        name=_name(obj),
        description=_optional_str(obj.get("description")),
        indicator_type=_indicator_type(pattern),
        value=_extract_indicator_value(pattern),
        pattern=pattern if isinstance(pattern, str) else None,
        valid_from=_date_only(obj.get("valid_from")),
        valid_until=_date_only(obj.get("valid_until")),
        source=_source(obj),
    )


def map_vulnerability(obj: dict[str, Any], context) -> Vulnerability:
    external_id = _external_id(obj)
    name = obj.get("name") or external_id or obj.get("id", "Unnamed vulnerability")

    return Vulnerability(
        name=str(name),
        description=_optional_str(obj.get("description")),
        taxonomy_ref=_taxonomy_ref(obj, "stixVulnerability"),
        external_id=external_id,
        severity=_map_severity(obj.get("x_severity") or obj.get("severity")),
        cvss_score=_cvss_score(obj),
        source=_source(obj),
    )


def map_relationship(obj: dict[str, Any], context) -> list[GenericStixRelationship]:
    """Map a STIX Relationship SRO into a generic metamodel relationship."""
    source_ref = obj.get("source_ref")
    target_ref = obj.get("target_ref")
    relationship_type = obj.get("relationship_type", "related-to")

    if not isinstance(source_ref, str) or not isinstance(target_ref, str):
        context.skipped_relationships.append(
            {
                "id": str(obj.get("id", "<missing-id>")),
                "type": "relationship",
                "relationship_type": str(relationship_type),
                "reason": "relationship is missing source_ref or target_ref",
            }
        )
        return []

    source_entity = context.stix_to_entity.get(source_ref)
    target_entity = context.stix_to_entity.get(target_ref)

    if source_entity is None or target_entity is None:
        context.skipped_relationships.append(
            {
                "id": str(obj.get("id", "<missing-id>")),
                "type": "relationship",
                "relationship_type": str(relationship_type),
                "source_ref": source_ref,
                "target_ref": target_ref,
                "reason": "source_ref or target_ref was not mapped to a metamodel entity",
            }
        )
        return []

    return [
        GenericStixRelationship(
            source_entity=source_entity,
            target_entity=target_entity,
            stix_relationship_type=str(relationship_type),
            stix_id=obj.get("id") if isinstance(obj.get("id"), str) else None,
            raw=obj,
        )
    ]


def map_sighting(obj: dict[str, Any], context) -> list[GenericStixRelationship]:
    """Map a STIX Sighting SRO into one or more generic relationships.

    A STIX sighting asserts that something was seen. The parser creates one
    generic edge from `sighting_of_ref` to each available target in
    `observed_data_refs` and `where_sighted_refs`. If no target references are
    available, the sighting is reported as skipped.
    """
    sighting_of_ref = obj.get("sighting_of_ref")
    if not isinstance(sighting_of_ref, str):
        context.skipped_relationships.append(
            {
                "id": str(obj.get("id", "<missing-id>")),
                "type": "sighting",
                "reason": "sighting is missing sighting_of_ref",
            }
        )
        return []

    source_entity = context.stix_to_entity.get(sighting_of_ref)
    if source_entity is None:
        context.skipped_relationships.append(
            {
                "id": str(obj.get("id", "<missing-id>")),
                "type": "sighting",
                "sighting_of_ref": sighting_of_ref,
                "reason": "sighting_of_ref was not mapped to a metamodel entity",
            }
        )
        return []

    target_refs = []
    target_refs.extend(_as_str_list(obj.get("observed_data_refs")))
    target_refs.extend(_as_str_list(obj.get("where_sighted_refs")))

    relationships: list[GenericStixRelationship] = []

    for target_ref in target_refs:
        target_entity = context.stix_to_entity.get(target_ref)
        if target_entity is None:
            context.skipped_relationships.append(
                {
                    "id": str(obj.get("id", "<missing-id>")),
                    "type": "sighting",
                    "sighting_of_ref": sighting_of_ref,
                    "target_ref": target_ref,
                    "reason": "sighting target reference was not mapped to a metamodel entity",
                }
            )
            continue

        relationships.append(
            GenericStixRelationship(
                source_entity=source_entity,
                target_entity=target_entity,
                stix_relationship_type="sighting",
                stix_id=obj.get("id") if isinstance(obj.get("id"), str) else None,
                raw=obj,
            )
        )

    if not target_refs:
        context.skipped_relationships.append(
            {
                "id": str(obj.get("id", "<missing-id>")),
                "type": "sighting",
                "sighting_of_ref": sighting_of_ref,
                "reason": "sighting has no observed_data_refs or where_sighted_refs target",
            }
        )

    return relationships


def _name(obj: dict[str, Any]) -> str:
    value = obj.get("name")
    if isinstance(value, str) and value.strip():
        return value

    value = obj.get("value")
    if isinstance(value, str) and value.strip():
        return value

    value = obj.get("id")
    if isinstance(value, str) and value.strip():
        return value

    return "Unnamed STIX object"


def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _source(obj: dict[str, Any]) -> str:
    stix_id = obj.get("id", "<missing-id>")
    spec_version = obj.get("spec_version")
    if spec_version:
        return f"STIX {spec_version}: {stix_id}"
    return f"STIX: {stix_id}"


def _aliases(obj: dict[str, Any]) -> list[str]:
    aliases = obj.get("aliases")
    if aliases is None:
        aliases = obj.get("x_mitre_aliases")
    return _as_str_list(aliases)


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _first_str(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                return item
    return None


def _date_only(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) < 10:
        return None

    candidate = value[:10]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", candidate):
        return candidate

    return None


def _external_id(obj: dict[str, Any]) -> str | None:
    for ref in obj.get("external_references", []) or []:
        if isinstance(ref, dict) and isinstance(ref.get("external_id"), str):
            return ref["external_id"]
    return None


def _external_source(obj: dict[str, Any]) -> str | None:
    for ref in obj.get("external_references", []) or []:
        if isinstance(ref, dict) and isinstance(ref.get("source_name"), str):
            return ref["source_name"]
    return None


def _taxonomy_ref(obj: dict[str, Any], fallback_taxonomy: str) -> str:
    external_id = _external_id(obj)
    external_source = _external_source(obj)

    if external_id and external_source:
        return f"{_safe_taxonomy_name(external_source)}:{external_id}"

    stix_id = obj.get("id")
    if isinstance(stix_id, str):
        return f"{fallback_taxonomy}:{_safe_concept_id(stix_id)}"

    return f"{fallback_taxonomy}:unknown"


def _safe_taxonomy_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", value.strip())
    cleaned = cleaned.strip("_")
    return cleaned or "external"


def _safe_concept_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def _indicator_type(pattern: Any) -> str:
    if not isinstance(pattern, str):
        return "unknown"

    lower = pattern.lower()

    if "ipv4-addr:value" in lower or "ipv6-addr:value" in lower:
        return "ip"
    if "domain-name:value" in lower:
        return "domain"
    if "url:value" in lower:
        return "url"
    if "file:hashes" in lower:
        return "hash"
    if "email-addr:value" in lower:
        return "email"
    if "windows-registry-key:key" in lower:
        return "registry"

    return "unknown"


def _extract_indicator_value(pattern: Any) -> str | None:
    if not isinstance(pattern, str):
        return None

    match = re.search(r"=\s*'([^']+)'", pattern)
    if match:
        return match.group(1)

    match = re.search(r'=\s*"([^"]+)"', pattern)
    if match:
        return match.group(1)

    return None


def _map_sophistication(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.lower().replace("-", "_").replace(" ", "_")

    if normalized in {"none", "minimal", "low"}:
        return "low"
    if normalized in {"intermediate", "medium"}:
        return "medium"
    if normalized in {"advanced", "expert", "strategic"}:
        return "advanced"

    return "unknown"


def _map_tool_type(value: str | None) -> str:
    if value is None:
        return "unknown"

    normalized = value.lower().replace("-", "_").replace(" ", "_")

    if normalized in {"command_and_control", "remote_access", "remote_access_trojan"}:
        return "command_and_control"
    if "credential" in normalized:
        return "credential_tool"
    if "scanner" in normalized or "reconnaissance" in normalized:
        return "scanner"
    if "exploit" in normalized:
        return "exploit_kit"
    if "living" in normalized:
        return "living_off_the_land"

    return "custom_tool"


def _map_severity(value: Any) -> str | None:
    if not isinstance(value, str):
        return None

    normalized = value.lower().strip()

    if normalized in {"low", "medium", "high", "critical"}:
        return normalized

    return "unknown"


def _cvss_score(obj: dict[str, Any]) -> float | None:
    for key in ("cvss_score", "x_cvss_score", "x_cvss_v3_score"):
        value = obj.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            score = float(value)
            if 0.0 <= score <= 10.0:
                return score
    return None
