"""STIX constants used by the extensible STIX parser.

The official OASIS CTI introduction to STIX 2.1 lists 18 STIX Domain Objects
and two STIX Relationship Objects. The parser also includes common STIX 2.1
Cyber-observable Object and Meta Object type names so they can be preserved as
generic STIX entities when present in bundles.
"""

from __future__ import annotations


STIX_DOMAIN_OBJECT_TYPES: dict[str, str] = {
    "attack-pattern": "Attack Pattern",
    "campaign": "Campaign",
    "course-of-action": "Course of Action",
    "grouping": "Grouping",
    "identity": "Identity",
    "indicator": "Indicator",
    "infrastructure": "Infrastructure",
    "intrusion-set": "Intrusion Set",
    "location": "Location",
    "malware": "Malware",
    "malware-analysis": "Malware Analysis",
    "note": "Note",
    "observed-data": "Observed Data",
    "opinion": "Opinion",
    "report": "Report",
    "threat-actor": "Threat Actor",
    "tool": "Tool",
    "vulnerability": "Vulnerability",
}

STIX_RELATIONSHIP_OBJECT_TYPES: dict[str, str] = {
    "relationship": "Relationship",
    "sighting": "Sighting",
}

STIX_CYBER_OBSERVABLE_OBJECT_TYPES: dict[str, str] = {
    "artifact": "Artifact",
    "autonomous-system": "Autonomous System",
    "directory": "Directory",
    "domain-name": "Domain Name",
    "email-addr": "Email Address",
    "email-message": "Email Message",
    "file": "File",
    "ipv4-addr": "IPv4 Address",
    "ipv6-addr": "IPv6 Address",
    "mac-addr": "MAC Address",
    "mutex": "Mutex",
    "network-traffic": "Network Traffic",
    "process": "Process",
    "software": "Software",
    "url": "URL",
    "user-account": "User Account",
    "windows-registry-key": "Windows Registry Key",
    "x509-certificate": "X.509 Certificate",
}

STIX_META_OBJECT_TYPES: dict[str, str] = {
    "extension-definition": "Extension Definition",
    "language-content": "Language Content",
    "marking-definition": "Marking Definition",
}

STIX_CONTAINER_OBJECT_TYPES: dict[str, str] = {
    "bundle": "Bundle",
}

STIX_OBJECT_TYPES: dict[str, str] = {
    **STIX_DOMAIN_OBJECT_TYPES,
    **STIX_CYBER_OBSERVABLE_OBJECT_TYPES,
    **STIX_META_OBJECT_TYPES,
    **STIX_CONTAINER_OBJECT_TYPES,
}

STIX_EDGE_OBJECT_TYPES: dict[str, str] = {
    **STIX_RELATIONSHIP_OBJECT_TYPES,
}

STIX_STANDARD_TYPES: dict[str, str] = {
    **STIX_OBJECT_TYPES,
    **STIX_EDGE_OBJECT_TYPES,
}
