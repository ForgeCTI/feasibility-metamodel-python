"""Case Study 04 - Exploitation of a Vulnerable Enterprise System.

A fictional industrial manufacturer is targeted through an exposed order portal
and an overprivileged maintenance script. The scenario illustrates how software
and configuration vulnerabilities can threaten an organizational business asset
and its corresponding security requirements.

All organizations, vulnerabilities, tools, and incident details are fictional.
"""

from metamodel.core.Model import Model

# Organization entities
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.BusinessRequirement import BusinessRequirement
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.entities.AssetSecurityRequirement import (
    AssetSecurityRequirement,
)
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement

# Infrastructure entities
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.OS import OS
from metamodel.infrastructure.entities.OSInstance import OSInstance
from metamodel.infrastructure.entities.Code import Code

# CyberThreat entities
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration

# Organization relationships
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.hasBusinessRequirement import hasBusinessRequirement
from metamodel.organization.rels.drivesSecurityRequirement import (
    drivesSecurityRequirement,
)
from metamodel.organization.rels.hasSecurityRequirement import hasSecurityRequirement
from metamodel.organization.rels.implementsRequirement import implementsRequirement

# Infrastructure relationships
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.hostsResource import hostsResource
from metamodel.infrastructure.rels.runsOS import runsOS
from metamodel.infrastructure.rels.osInstanceOf import osInstanceOf
from metamodel.infrastructure.rels.runsApp import runsApp
from metamodel.infrastructure.rels.applicationInstanceOf import applicationInstanceOf

# CyberThreat relationships
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.followedBy import followedBy
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.exploitsVulnerability import exploitsVulnerability
from metamodel.cyberThreat.rels.affectsApplication import affectsApplication
from metamodel.cyberThreat.rels.affectsOS import affectsOS
from metamodel.cyberThreat.rels.affectsCode import affectsCode
from metamodel.cyberThreat.rels.compromises import compromises
from metamodel.cyberThreat.rels.targetsResource import targetsResource
from metamodel.cyberThreat.rels.violates import violates
from metamodel.cyberThreat.rels.employsTool import employsTool
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf
from metamodel.cyberThreat.rels.hasConfig import hasConfig
from metamodel.cyberThreat.rels.requiresConfig import requiresConfig


def build_model() -> Model:
    """Build the simulated Meridian Industrial Systems attack scenario."""
    model = Model()

    # Organization scenario entities
    organization = model.add(
        Organization(
            name='Meridian Industrial Systems',
            description=(
                'Fictional manufacturer of industrial components whose customer '
                'orders are managed through a corporate web portal.'
            ),
            legal_name='Meridian Industrial Systems S.r.l.',
            short_name='MIS',
            website='https://meridian-industrial.example',
            organization_size='Medium',
            criticality='High',
            maturity_level='Intermediate',
            source="Synthetic case study data",
        )
    )

    sector = model.add(
        Sector(
            name='Industrial Components Manufacturing',
            description=(
                'Manufacture and machining of industrial metal components, '
                'classified under the NACE system.'
            ),
            sector_code='25.62',
            sector_standard='NACE',
            sector_standard_version='Rev. 2',
            source="Synthetic case study data",
        )
    )

    business_requirement = model.add(
        BusinessRequirement(
            name='Reliable Industrial Order Processing',
            description=(
                'Business need to maintain reliable, uninterrupted processing and '
                'tracking of customer orders.'
            ),
            priority='High',
            source="Synthetic case study data",
        )
    )

    asset = model.add(
        Asset(
            name='Order Fulfilment Process',
            description=(
                'Business process responsible for receiving, confirming, and '
                'fulfilling industrial customer orders.'
            ),
            source="Synthetic case study data",
        )
    )

    asset_security_requirement = model.add(
        AssetSecurityRequirement(
            name='Order Records Integrity Control',
            description=(
                'Asset-specific requirement to prevent unauthorized changes to '
                'order records and their processing status.'
            ),
            source="Synthetic case study data",
        )
    )

    security_requirement = model.add(
        SecurityRequirement(
            name='Integrity of Order Records',
            description=(
                'General requirement that order records be protected against '
                'unauthorized or untracked modifications.'
            ),
            requirement_type='integrity',
            source="Synthetic case study data",
        )
    )

    # Infrastructure scenario entities
    infrastructure = model.add(
        Infrastructure(
            name='Meridian Order Processing Infrastructure',
            description=(
                'Production IT environment supporting the company order portal, '
                'maintenance scripts, and related services.'
            ),
            environment_type='Production',
            scope='Industrial orders and maintenance operations',
            source="Synthetic case study data",
        )
    )

    application_server = model.add(
        Node(
            name='Order Application Server',
            description=(
                'Corporate application server hosting the production order portal '
                'and its supporting services.'
            ),
            hostname='mis-order-app-01',
            ip_addresses=['192.0.2.44'],
            mac_addresses=['02:00:00:00:00:44'],
            fqdn='mis-order-app-01.meridian-industrial.example',
            source="Synthetic case study data",
        )
    )

    order_service = model.add(
        Resource(
            name='Order Management Service',
            description=(
                'Operational service that processes customer orders and updates '
                'their status within the enterprise.'
            ),
            source="Synthetic case study data",
        )
    )

    order_portal = model.add(
        Application(
            name='Meridian Order Portal',
            description=(
                'Fictional order-processing web application that depends on a '
                'shared software runtime component.'
            ),
            vendor='Meridian Internal Software',
            product='Order Portal',
            version='3.2.0',
            cpe='cpe:2.3:a:meridian:order_portal:3.2.0:*:*:*:*:*:*:*',
            source="Synthetic case study data",
        )
    )

    order_portal_instance = model.add(
        ApplicationInstance(
            name='Order Portal Production Instance',
            description=(
                'Specific production deployment of the Meridian Order Portal '
                'running on the application server.'
            ),
            version='3.2.0',
            runtime_state='Running',
            source="Synthetic case study data",
        )
    )

    server_os = model.add(
        OS(
            name='Meridian Server OS',
            description=(
                'Fictional server operating system distribution supplying the '
                'same shared runtime component.'
            ),
            vendor='Meridian Systems Lab',
            product='Meridian Server OS',
            version='1.6',
            cpe='cpe:2.3:o:meridian:server_os:1.6:*:*:*:*:*:*:*',
            source="Synthetic case study data",
        )
    )

    server_os_instance = model.add(
        OSInstance(
            name='Order Server OS Installation',
            description=(
                'Installed operating system instance supporting the order portal '
                'on the production server.'
            ),
            version='1.6',
            build='1.6.42',
            patch_level='October 2026 baseline',
            support_status='Supported',
            source="Synthetic case study data",
        )
    )

    maintenance_script = model.add(
        Code(
            name='Order Maintenance Script',
            description=(
                'Python maintenance script used by authorized administrators for '
                'controlled updates to order records.'
            ),
            language='Python',
            version='1.3.0',
            repository_url=(
                'https://git.meridian-industrial.example/ops/order-maintenance'
            ),
            source="Synthetic case study data",
        )
    )

    # CyberThreat scenario entities
    threat_actor = model.add(
        ThreatActor(
            name='Foundry Access Group',
            description=(
                'Fictional financially motivated threat group responsible for the '
                'simulated intrusion.'
            ),
            aliases=['Foundry Crew'],
            motivation='Financial gain',
            sophistication='Moderate',
            country='Unknown',
            source="Synthetic case study data",
        )
    )

    threat = model.add(
        Threat(
            name='Order Portal Compromise',
            description=(
                'Coordinated attempt to gain unauthorized access to the order '
                'portal and manipulate customer orders.'
            ),
            objective='Alter order records and disrupt order fulfilment',
            first_seen='2026-10-20',
            last_seen='2026-10-22',
            source="Synthetic case study data",
        )
    )

    portal_exploitation_step = model.add(
        ThreatStep(
            name='Order Portal Exploitation',
            description=(
                'Initial attack step exploiting weak input validation to bypass '
                'access controls in the public order portal.'
            ),
            phase='Initial Access',
            objective='Gain unauthorized access to the order portal',
            preconditions=['Portal is reachable',
             'Shared runtime vulnerability is unpatched'],
            postconditions=['Unauthorized portal functions accessible'],
            source="Synthetic case study data",
        )
    )

    maintenance_abuse_step = model.add(
        ThreatStep(
            name='Maintenance Script Abuse',
            description=(
                'Follow-on step abusing excessive maintenance-script privileges '
                'to alter order records without authorization.'
            ),
            phase='Execution',
            objective='Change order status without authorization',
            preconditions=['Portal access achieved',
             'Maintenance script privileges are excessive'],
            postconditions=['Order records can be modified without authorization'],
            source="Synthetic case study data",
        )
    )

    portal_exploitation_ttp = model.add(
        TTP(
            name='Exploit Public-Facing Application',
            description=(
                'MITRE ATT&CK technique describing exploitation of an '
                'internet-facing application to obtain access.'
            ),
            external_id='T1190',
            tactic='Initial Access',
            technique='Exploit Public-Facing Application',
            subtechnique=None,
            source="MITRE ATT&CK (scenario technique mapping)",
        )
    )

    python_execution_ttp = model.add(
        TTP(
            name='Command and Scripting Interpreter: Python',
            description=(
                'MITRE ATT&CK technique describing adversarial execution of '
                'Python commands or scripts.'
            ),
            external_id='T1059.006',
            tactic='Execution',
            technique='Command and Scripting Interpreter',
            subtechnique='Python',
            source="MITRE ATT&CK (scenario technique mapping)",
        )
    )

    software_vulnerability = model.add(
        SoftwareVulnerability(
            name='Shared Runtime Input Validation Weakness',
            description=(
                'Fictional weakness in input validation within a shared runtime '
                'used by the application and operating system.'
            ),
            external_id='MIS-SW-001',
            severity='High',
            cvss_score=8.8,
            # Synthetic vulnerability: no official CVE has been assigned.
            cve_id=None,
            cwe_id='CWE-20',
            affected_versions=['Shared Runtime 2.5.0'],
            source="Synthetic case study data",
        )
    )

    config_vulnerability = model.add(
        ConfigVulnerability(
            name='Insecure Maintenance Script Permissions',
            description=(
                'Fictional configuration weakness granting more privileges than '
                'necessary to the order maintenance script.'
            ),
            external_id='MIS-CFG-001',
            severity='High',
            cvss_score=7.5,
            misconfiguration_type='Excessive Script Privileges',
            detectability='Moderate',
            source="Synthetic case study data",
        )
    )

    attack_tool = model.add(
        AttackTool(
            name='Remote Order Manipulation Utility',
            description=(
                'Fictional post-exploitation utility able to interact with '
                'compromised portal functions and change orders.'
            ),
            aliases=['order-admin-kit'],
            tool_type='Post-exploitation utility',
            capabilities=['Remote command execution', 'Order status modification'],
            source="Synthetic case study data",
        )
    )

    attack_tool_instance = model.add(
        AttackToolInstance(
            name='Order Server Intrusion Utility Instance',
            description=(
                'Concrete simulated deployment of the intrusion utility on the '
                'compromised order application server.'
            ),
            observed_version='0.9.0',
            hashes=['32a3edd3a3d4545d3d67cfab23f986ec4f748ca6d63ed733a2ee606f47e9b1a2'],
            first_seen='2026-10-20',
            last_seen='2026-10-22',
            source="Synthetic case study data",
        )
    )

    attack_tool_configuration = model.add(
        AttackToolConfiguration(
            name='Order Intrusion Utility Configuration',
            description=(
                'Simulated target-specific configuration governing the intrusion '
                'utility execution context.'
            ),
            configuration_type='Target-specific runtime configuration',
            parameters={'target_service': 'order-management',
             'execution_profile': 'maintenance-context'},
            persistence_enabled=False,
            stealth_level='Low',
            source="Synthetic case study data",
        )
    )

    # Organization relationships
    model.add(operatesIn(organization, sector))
    model.add(hasBusinessRequirement(organization, business_requirement))
    model.add(drivesSecurityRequirement(business_requirement, asset_security_requirement))
    model.add(hasSecurityRequirement(asset, asset_security_requirement))
    model.add(implementsRequirement(asset_security_requirement, security_requirement))

    # Infrastructure relationships
    model.add(manages(organization, infrastructure))
    model.add(madeBy(infrastructure, application_server))
    model.add(hostsResource(application_server, order_service))
    model.add(runsOS(application_server, server_os_instance))
    model.add(osInstanceOf(server_os_instance, server_os))
    model.add(runsApp(application_server, order_portal_instance))
    model.add(applicationInstanceOf(order_portal_instance, order_portal))

    # CyberThreat relationships
    model.add(initiates(threat_actor, threat))
    model.add(startsWith(threat, portal_exploitation_step))
    model.add(followedBy(portal_exploitation_step, maintenance_abuse_step))
    model.add(implementsTTP(portal_exploitation_step, portal_exploitation_ttp))
    model.add(implementsTTP(maintenance_abuse_step, python_execution_ttp))
    model.add(exploits(portal_exploitation_step, software_vulnerability))
    model.add(exploits(maintenance_abuse_step, config_vulnerability))
    model.add(exploitsVulnerability(portal_exploitation_ttp, software_vulnerability))
    model.add(exploitsVulnerability(python_execution_ttp, config_vulnerability))
    model.add(affectsApplication(software_vulnerability, order_portal))
    model.add(affectsOS(software_vulnerability, server_os))
    model.add(affectsCode(config_vulnerability, maintenance_script))
    # Step 1 bypasses the integrity protection; Step 2 alters order records.
    model.add(compromises(portal_exploitation_step, asset_security_requirement))
    model.add(compromises(maintenance_abuse_step, asset_security_requirement))
    model.add(targetsResource(portal_exploitation_step, order_service))
    model.add(targetsResource(maintenance_abuse_step, order_service))
    model.add(violates(portal_exploitation_ttp, security_requirement))
    model.add(violates(python_execution_ttp, security_requirement))
    model.add(employsTool(maintenance_abuse_step, attack_tool_instance))
    model.add(toolInstanceOf(attack_tool_instance, attack_tool))
    model.add(hasConfig(attack_tool_instance, attack_tool_configuration))
    model.add(requiresConfig(attack_tool, attack_tool_configuration))

    return model


def main() -> None:
    """Run the fourth case study and print its validation outcome."""
    model = build_model()
    report = model.validate()

    print("Case Study 4")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
