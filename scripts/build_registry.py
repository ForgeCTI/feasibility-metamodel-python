"""Usage (from the repository root): python scripts/build_registry.py src/metamodel

Generate relationship modules, package __init__ files, and registry_data.py from one spec.

Each row: (class name, package, label, source, target, source end, target end, extra)
Multiplicities follow the paper's figures (source end, target end).
"""
import os, sys
ROOT = sys.argv[1]

ENT_PKG = {}
for pkg, names in {
    'organization': ['Organization', 'Sector', 'HomeCountry', 'InternationalBody', 'BusinessRequirement',
                     'SecurityRequirement', 'Asset', 'AssetSecurityRequirement'],
    'infrastructure': ['Infrastructure', 'Node', 'NodeType', 'Port', 'Connection', 'Resource', 'Code', 'Data', 'DataType',
                       'User', 'UserType', 'Account', 'PrivilegeLevel', 'Application', 'ApplicationInstance', 'OS',
                       'OSInstance', 'SecurityControl', 'SecurityControlType'],
    'cyberThreat': ['ThreatActor', 'Adversary', 'AdversaryType', 'Expertise', 'Threat', 'ThreatStep', 'Campaign', 'TTP',
                    'Indicator', 'Vulnerability', 'SoftwareVulnerability', 'ConfigVulnerability', 'HumanVulnerability',
                    'AttackTool', 'AttackToolInstance', 'AttackToolConfiguration'],
}.items():
    for n in names:
        ENT_PKG[n] = pkg

GRANT = dict(attrs={'privilege_level': 'PrivilegeLevel'},
             doc='The association class PrivilegeLevel is the attribute ``privilege_level``.')
RELS = [
 # organization
 ('operatesIn', 'organization', 'operatesIn', 'Organization', 'Sector', '0..*', '1..*', {}),
 ('basedIn', 'organization', 'basedIn', 'Organization', 'HomeCountry', '0..*', '1..*', {}),
 ('countryPartOf', 'organization', 'partOf', 'HomeCountry', 'InternationalBody', '1..*', '0..*', {'legacy': ['partsOf']}),
 ('hasBusinessRequirement', 'organization', 'hasBusinessRequirement', 'Organization', 'BusinessRequirement', '1', '1..*', {}),
 ('drivesSecurityRequirement', 'organization', 'drivesSecurityRequirement', 'BusinessRequirement', 'AssetSecurityRequirement', '1', '1..*', {}),
 ('hasSecurityRequirement', 'organization', 'hasSecurityRequirement', 'Asset', 'AssetSecurityRequirement', '1', '1..*', {}),
 ('implementsRequirement', 'organization', 'implementationOf', 'AssetSecurityRequirement', 'SecurityRequirement', '0..*', '1', {}),
 # infrastructure
 ('manages', 'infrastructure', 'manages', 'Organization', 'Infrastructure', '1', '1..*', {}),
 ('madeBy', 'infrastructure', 'madeBy', 'Infrastructure', 'Node', '1', '1..*', {}),
 ('usedBy', 'infrastructure', 'usedBy', 'Infrastructure', 'User', '1..*', '1..*', {}),
 ('hasNodeType', 'infrastructure', 'hasNodeType', 'Node', 'NodeType', '0..*', '1', {}),
 ('runsOS', 'infrastructure', 'runsOS', 'Node', 'OSInstance', '1', '0..1', {}),
 ('runsApp', 'infrastructure', 'runsApp', 'Node', 'ApplicationInstance', '1', '0..*', {}),
 ('runs', 'infrastructure', 'runs', 'Node', 'Node', '0..1', '0..*', {'doc': 'A node runs another node, e.g. a container or a virtual machine.'}),
 ('hostsResource', 'infrastructure', 'hostsResource', 'Node', 'Resource', '1..*', '1..*',
  {'counts': ('runsApp', 'runsOS'), 'doc': 'Application and OS instances run by a node (runsApp, runsOS) count as hosted resources.'}),
 ('exposesPort', 'infrastructure', 'exposesPort', 'Node', 'Port', '1', '0..*', {}),
 ('isSource', 'infrastructure', 'isSource', 'Node', 'Connection', '0..1', '0..*', {}),
 ('isDestination', 'infrastructure', 'isDestination', 'Node', 'Connection', '0..1', '0..*', {}),
 ('hasDestinationPort', 'infrastructure', 'hasDestinationPort', 'Connection', 'Port', '0..*', '1', {}),
 ('uses', 'infrastructure', 'uses', 'ApplicationInstance', 'Port', '0..1', '0..*', {'legacy': ['listensOn'], 'doc': 'An application instance listens on a port.'}),
 ('applicationInstanceOf', 'infrastructure', 'instanceOf', 'ApplicationInstance', 'Application', '0..*', '1', {}),
 ('osInstanceOf', 'infrastructure', 'instanceOf', 'OSInstance', 'OS', '0..*', '1', {}),
 ('hasUserType', 'infrastructure', 'hasUserType', 'User', 'UserType', '0..*', '1', {}),
 ('hasAccount', 'infrastructure', 'hasAccount', 'User', 'Account', '1', '0..*', {}),
 ('grantsAccessToNode', 'infrastructure', 'grantsAccessTo', 'Account', 'Node', '0..*', '0..*', GRANT),
 ('grantsAccessToResource', 'infrastructure', 'grantsAccessTo', 'Account', 'Resource', '0..*', '1..*', GRANT),
 ('requiresPrivilegeLevel', 'infrastructure', 'requiresPrivilegeLevel', 'Resource', 'PrivilegeLevel', '0..*', '0..1', {}),
 ('hasDataType', 'infrastructure', 'hasDataType', 'Data', 'DataType', '0..*', '1', {'legacy': ['hasInformationType']}),
 ('securityControlInstanceOf', 'infrastructure', 'instanceOf', 'SecurityControl', 'SecurityControlType', '0..*', '1', {}),
 ('protectsNode', 'infrastructure', 'protects', 'SecurityControl', 'Node', '0..*', '0..*', {}),
 ('protectsUser', 'infrastructure', 'protects', 'SecurityControl', 'User', '0..*', '0..*', {}),
 ('protectsAccount', 'infrastructure', 'protects', 'SecurityControl', 'Account', '0..*', '0..*', {}),
 ('protectsResource', 'infrastructure', 'protects', 'SecurityControl', 'Resource', '0..*', '0..*', {}),
 ('mitigates', 'infrastructure', 'mitigates', 'SecurityControl', 'Vulnerability', '0..*', '0..*', {}),
 ('counters', 'infrastructure', 'counters', 'SecurityControlType', 'TTP', '0..*', '0..*',
  {'doc': 'Asserted only when the control type prevents the technique by design (curated).'}),
 # cyber threat
 ('initiates', 'cyberThreat', 'initiates', 'ThreatActor', 'Threat', '1', '1..*', {}),
 ('relatedTo', 'cyberThreat', 'relatedTo', 'ThreatActor', 'Adversary', '1..*', '0..*', {}),
 ('hasExpertise', 'cyberThreat', 'hasExpertise', 'ThreatActor', 'Expertise', '0..*', '0..1', {}),
 ('aliasOf', 'cyberThreat', 'alias', 'ThreatActor', 'ThreatActor', '0..*', '0..*', {}),
 ('hasAdversaryType', 'cyberThreat', 'hasAdversaryType', 'Adversary', 'AdversaryType', '0..*', '1..*', {}),
 ('threatPartOf', 'cyberThreat', 'partOf', 'Threat', 'Campaign', '1..*', '0..1', {'legacy': ['partsOf']}),
 ('startsWith', 'cyberThreat', 'startsWith', 'Threat', 'ThreatStep', '0..*', '1..*',
  {'doc': 'Paper figure: 1 at the Threat end, which would make every step a first step; relaxed to 0..* (a step may start several threats).'}),
 ('targetsSector', 'cyberThreat', 'focusesOn', 'Campaign', 'Sector', '0..*', '0..*', {}),
 ('focusesOnCountry', 'cyberThreat', 'focusesOn', 'Campaign', 'HomeCountry', '0..*', '0..*', {}),
 ('targetsInternationalBody', 'cyberThreat', 'focusesOn', 'Campaign', 'InternationalBody', '0..*', '0..*', {}),
 ('followedBy', 'cyberThreat', 'followedBy', 'ThreatStep', 'ThreatStep', '0..*', '0..*', {}),
 ('implementsTTP', 'cyberThreat', 'implements', 'ThreatStep', 'TTP', '0..*', '1', {}),
 ('exploits', 'cyberThreat', 'exploits', 'ThreatStep', 'Vulnerability', '0..*', '0..*', {}),
 ('targetsResource', 'cyberThreat', 'targetsResource', 'ThreatStep', 'Resource', '0..*', '0..*', {}),
 ('compromises', 'cyberThreat', 'compromises', 'ThreatStep', 'AssetSecurityRequirement', '0..*', '0..*', {}),
 ('employsTool', 'cyberThreat', 'employs', 'ThreatStep', 'AttackToolInstance', '0..*', '0..*', {}),
 ('exploitsVulnerability', 'cyberThreat', 'exploitsVulnerability', 'TTP', 'Vulnerability', '0..*', '0..*', {}),
 ('violates', 'cyberThreat', 'violates', 'TTP', 'SecurityRequirement', '0..*', '0..*', {}),
 ('toolInstanceOf', 'cyberThreat', 'instanceOf', 'AttackToolInstance', 'AttackTool', '0..*', '1', {}),
 ('hasConfig', 'cyberThreat', 'hasConfig', 'AttackToolInstance', 'AttackToolConfiguration', '0..*', '0..*', {}),
 ('deploysTool', 'cyberThreat', 'deploys', 'AttackToolInstance', 'AttackToolInstance', '0..*', '0..*', {}),
 ('producesIndicator', 'cyberThreat', 'produces', 'AttackToolInstance', 'Indicator', '0..1', '0..*', {}),
 ('associatedToTool', 'cyberThreat', 'associatedTo', 'Indicator', 'AttackToolInstance', '0..*', '0..1', {}),
 ('requiresConfig', 'cyberThreat', 'requires', 'AttackTool', 'AttackToolConfiguration', '0..*', '0..*', {}),
 ('requiresExpertise', 'cyberThreat', 'requiresExpertise', 'AttackTool', 'Expertise', '0..*', '0..1', {}),
 ('affectsUser', 'cyberThreat', 'affects', 'HumanVulnerability', 'User', '0..*', '1..*', {}),
 ('affectsCode', 'cyberThreat', 'affects', 'ConfigVulnerability', 'Code', '0..*', '0..*', {}),
 ('affectsAccount', 'cyberThreat', 'affects', 'ConfigVulnerability', 'Account', '0..*', '0..*', {}),
 ('affectsOS', 'cyberThreat', 'affects', 'SoftwareVulnerability', 'OS', '0..*', '1..*', {}),
 ('affectsApplication', 'cyberThreat', 'affects', 'SoftwareVulnerability', 'Application', '0..*', '1..*', {}),
]

def mod(n): return f'metamodel.{ENT_PKG[n]}.entities.{n}'

def write_rel(r):
    cls, pkg, label, src, tgt, sc, tc, extra = r
    imports = {src, tgt} | set(extra.get('attrs', {}).values())
    imp = ''.join(f'from {mod(n)} import {n}\n' for n in sorted(imports))
    doc = f'{src} --{label}--> {tgt}.'
    if extra.get('doc'):
        doc += '\n\n    ' + extra['doc']
    body = f'''from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
{imp}

class {cls}(BaseRelationship):
    """{doc}"""

    label = {label!r}
    source_type = {src}
    target_type = {tgt}
    source_cardinality = {sc!r}
    target_cardinality = {tc!r}
'''
    if extra.get('attrs'):
        body += f"    _domain_attributes = ({', '.join(repr(a) for a in extra['attrs'])},)\n"
        body += '    _entity_attributes = {' + ', '.join(f'{a!r}: {t}' for a, t in extra['attrs'].items()) + '}\n'
    if extra.get('counts'):
        body += f"    cardinality_counts = {tuple(extra['counts'])!r}\n"
    open(os.path.join(ROOT, pkg, 'rels', cls + '.py'), 'w').write(body)

# remove obsolete relationship modules
keep = {r[0] for r in RELS}
removed = []
for pkg in ('organization', 'infrastructure', 'cyberThreat'):
    d = os.path.join(ROOT, pkg, 'rels')
    for f in os.listdir(d):
        if f.endswith('.py') and f != '__init__.py' and f[:-3] not in keep:
            os.remove(os.path.join(d, f)); removed.append(f[:-3])
for r in RELS:
    write_rel(r)
for pkg in ('organization', 'infrastructure', 'cyberThreat'):
    names = [r[0] for r in RELS if r[1] == pkg]
    s = ''.join(f'from metamodel.{pkg}.rels.{n} import {n}\n' for n in names)
    s += '\n__all__ = [' + ', '.join(repr(n) for n in names) + ']\n'
    open(os.path.join(ROOT, pkg, 'rels', '__init__.py'), 'w').write(s)
    ents = [n for n, p in ENT_PKG.items() if p == pkg]
    s = ''.join(f'from metamodel.{pkg}.entities.{n} import {n}\n' for n in ents)
    s += '\n__all__ = [' + ', '.join(repr(n) for n in ents) + ']\n'
    open(os.path.join(ROOT, pkg, 'entities', '__init__.py'), 'w').write(s)

# registry_data.py
ent_imports = [(n, mod(n), n) for n in ENT_PKG]
rel_imports = [(r[0], f'metamodel.{r[1]}.rels.{r[0]}', r[0]) for r in RELS]
aliases = []
for cls, pkg, label, src, tgt, sc, tc, extra in RELS:
    for lab in dict.fromkeys([label, cls] + extra.get('legacy', [])):
        aliases.append((src, lab, tgt, cls))
LEGACY_ENT = [('Information', 'Data'), ('InformationType', 'DataType')]
LEGACY_REL = [('hasInformationType', 'hasDataType'), ('listensOn', 'uses')]
def fmt(lst):
    return '[\n' + ''.join(f'    {t!r},\n' for t in lst) + ']'
open(os.path.join(ROOT, 'registry_data.py'), 'w').write(
    '"""Registry of entity and relationship classes.\n\nGenerated by scripts/build_registry.py from the relationship specification; do not edit by hand.\n"""\n\n'
    f'ENTITY_IMPORTS = {fmt(ent_imports)}\n\nRELATIONSHIP_IMPORTS = {fmt(rel_imports)}\n\n'
    '# (source type, label, target type, relationship class)\n'
    f'RELATIONSHIP_ALIASES = {fmt(aliases)}\n\n'
    '# Names accepted by the importers for backward compatibility: (old name, new name)\n'
    f'LEGACY_ENTITY_TYPES = {fmt(LEGACY_ENT)}\n\nLEGACY_RELATIONSHIP_TYPES = {fmt(LEGACY_REL)}\n')
print('rels', len(RELS), 'removed', removed)
