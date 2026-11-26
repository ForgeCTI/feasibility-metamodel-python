"""Case Study 05 - Coordinated Cyber-Espionage Campaign.

A fictional Italian research institute is targeted by an espionage campaign.
The scenario illustrates actor alias correlation, virtualized infrastructure,
legitimate user access, an unclassified vulnerability, and multistage tool
deployment during the collection of confidential research documents.

All incident details, organizations, tools, and indicators are synthetic.
"""

from metamodel.core.Model import Model

# Organization entities
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.InternationalBody import InternationalBody

# Infrastructure entities
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Code import Code
from metamodel.infrastructure.entities.Information import Information

# CyberThreat entities
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance

# Organization relationships
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.basedIn import basedIn
from metamodel.organization.rels.countryPartOf import countryPartOf

# Infrastructure relationships
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.runs import runs
from metamodel.infrastructure.rels.usedBy import usedBy
from metamodel.infrastructure.rels.hasAccessTo import hasAccessTo
from metamodel.infrastructure.rels.runsApp import runsApp
from metamodel.infrastructure.rels.applicationInstanceOf import applicationInstanceOf
from metamodel.infrastructure.rels.applicationImplementsCode import (
    applicationImplementsCode,
)
from metamodel.infrastructure.rels.launches import launches
from metamodel.infrastructure.rels.accessesInformation import accessesInformation
from metamodel.infrastructure.rels.userAccessesInformation import (
    userAccessesInformation,
)

# CyberThreat relationships
from metamodel.cyberThreat.rels.aliasOf import aliasOf
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.threatPartOf import threatPartOf
from metamodel.cyberThreat.rels.focusesOnCountry import focusesOnCountry
from metamodel.cyberThreat.rels.targetsInternationalBody import targetsInternationalBody
from metamodel.cyberThreat.rels.targetsSector import targetsSector
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.followedBy import followedBy
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.employsTool import employsTool
from metamodel.cyberThreat.rels.deploysTool import deploysTool
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf
from metamodel.cyberThreat.rels.deployedTo import deployedTo


SYNTHETIC_SOURCE = "Synthetic case study data"


def build_model() -> Model:
    """Build the simulated Asterion Research Institute attack scenario."""
    model = Model()

    # Organization scenario entities
    organization = model.add(
        Organization(
            name='Asterion Research Institute',
            description=(
                'Fictional Italian research institute participating in international '
                'scientific programs.'
            ),
            legal_name='Asterion Research Institute S.r.l.',
            short_name='ARI',
            website='https://asterion-research.example',
            organization_size='Medium',
            criticality='High',
            maturity_level='Intermediate',
            source=SYNTHETIC_SOURCE,
        )
    )

    sector = model.add(
        Sector(
            name='Scientific Research and Development',
            description=(
                'Research and experimental development in natural sciences and '
                'engineering under NACE Rev. 2.'
            ),
            sector_code='72.19',
            sector_standard='NACE',
            sector_standard_version='Rev. 2',
            source=SYNTHETIC_SOURCE,
        )
    )

    country = model.add(
        HomeCountry(
            name='Italy',
            description=(
                'Country in which the research institute is based and on which the '
                'simulated campaign focuses.'
            ),
            iso2_code='IT',
            iso3_code='ITA',
            region='Southern Europe',
            source=SYNTHETIC_SOURCE,
        )
    )

    international_body = model.add(
        InternationalBody(
            name='European Research Cooperation Council',
            description=(
                'Fictional international body coordinating research programs involving '
                'Italy in this scenario.'
            ),
            acronym='ERCC',
            source=SYNTHETIC_SOURCE,
        )
    )


    # Infrastructure scenario entities
    infrastructure = model.add(
        Infrastructure(
            name='Asterion Research IT Infrastructure',
            description=(
                'Production environment supporting virtualized research document '
                'management services.'
            ),
            environment_type='Production',
            scope='Research document management and virtualized services',
            source=SYNTHETIC_SOURCE,
        )
    )

    physical_hypervisor = model.add(
        Node(
            name='Asterion Physical Hypervisor',
            description=(
                'Physical server hosting the virtual machine used for research '
                'document management.'
            ),
            hostname='ari-hv-01',
            ip_addresses=['192.0.2.50'],
            mac_addresses=['02:00:00:00:00:50'],
            fqdn='ari-hv-01.asterion-research.example',
            source=SYNTHETIC_SOURCE,
        )
    )

    document_vm = model.add(
        Node(
            name='Research Document VM',
            description=(
                'Virtual machine running the research portal on the physical '
                'hypervisor.'
            ),
            hostname='ari-doc-vm-01',
            ip_addresses=['192.0.2.51'],
            mac_addresses=['02:00:00:00:00:51'],
            fqdn='ari-doc-vm-01.asterion-research.example',
            source=SYNTHETIC_SOURCE,
        )
    )

    researcher = model.add(
        User(
            name='Asterion Researcher Account',
            description=(
                'Legitimate researcher account authorized to access the document VM '
                'and confidential research results; its session context is abused in '
                'the simulated attack.'
            ),
            username='e.serra',
            email='e.serra@asterion-research.example',
            role='Research Scientist',
            mfa_enabled=True,
            source=SYNTHETIC_SOURCE,
        )
    )

    research_portal = model.add(
        Application(
            name='Asterion Research Document Portal',
            description=(
                'Fictional internal application used to consult research '
                'documentation.'
            ),
            vendor='Asterion Internal Software',
            product='Research Document Portal',
            version='2.4.0',
            cpe='cpe:2.3:a:asterion:research_document_portal:2.4.0:*:*:*:*:*:*:*',
            source=SYNTHETIC_SOURCE,
        )
    )

    research_portal_instance = model.add(
        ApplicationInstance(
            name='Research Portal Production Instance',
            description=(
                'Production deployment of the research portal running on the document '
                'VM.'
            ),
            version='2.4.0',
            runtime_state='Running',
            source=SYNTHETIC_SOURCE,
        )
    )

    document_viewer = model.add(
        Code(
            name='Research Document Viewer',
            description=(
                'Python component launched by the researcher to consult restricted '
                'research documents.'
            ),
            language='Python',
            version='1.2.0',
            repository_url='https://git.asterion-research.example/apps/document-viewer',
            source=SYNTHETIC_SOURCE,
        )
    )

    research_results = model.add(
        Information(
            name='Confidential Research Results',
            description=(
                'Unpublished research results in PDF format, accessible to authorized '
                'researchers and sought by the attacker.'
            ),
            format='PDF',
            source=SYNTHETIC_SOURCE,
        )
    )


    # CyberThreat scenario entities
    threat_actor = model.add(
        ThreatActor(
            name='Silent Horizon Group',
            description=(
                'Primary CTI identity of the fictional actor responsible for the '
                'research espionage activity.'
            ),
            aliases=['Ghost Meridian'],
            motivation='Cyber-espionage',
            sophistication='High',
            country='Unknown',
            source=SYNTHETIC_SOURCE,
        )
    )

    threat_actor_alias = model.add(
        ThreatActor(
            name='Ghost Meridian',
            description=(
                'Alternative CTI identity referring to Silent Horizon Group, without a '
                'separate threat attribution.'
            ),
            aliases=['Silent Horizon Group'],
            motivation='Cyber-espionage',
            sophistication='High',
            country='Unknown',
            source=SYNTHETIC_SOURCE,
        )
    )

    campaign = model.add(
        Campaign(
            name='European Research Espionage Campaign',
            description=(
                'Fictional coordinated campaign targeting scientific research in Italy '
                'and its international research context.'
            ),
            first_seen='2026-11-01',
            last_seen='2026-11-08',
            status='Completed',
            objective='Acquire unpublished research data',
            source=SYNTHETIC_SOURCE,
        )
    )

    threat = model.add(
        Threat(
            name='Research Portal Espionage',
            description=(
                'Intrusion and collection activity against the research portal.'
            ),
            objective=(
                'Obtain unauthorized access to the research portal and collect '
                'confidential research results'
            ),
            first_seen='2026-11-02',
            last_seen='2026-11-06',
            source=SYNTHETIC_SOURCE,
        )
    )

    portal_compromise_step = model.add(
        ThreatStep(
            name='Research Portal Compromise',
            description=(
                'Initial compromise of the research portal through an unclassified '
                'weakness, followed by deployment of the first tool.'
            ),
            phase='Initial Access',
            objective='Establish unauthorized access',
            preconditions=[
                'Research portal is reachable',
                'Unclassified access weakness is present',
            ],
            postconditions=['Unauthorized access established', 'First tool instance deployed'],
            source=SYNTHETIC_SOURCE,
        )
    )

    document_collection_step = model.add(
        ThreatStep(
            name='Research Document Collection',
            description=(
                'Simulated collection of restricted research results by abusing an '
                'accessible research session with the second tool.'
            ),
            phase='Collection',
            objective='Collect confidential research results',
            preconditions=[
                'Unauthorized access established',
                'Collection tool deployed',
                'Research session accessible',
            ],
            postconditions=['Confidential research documents collected'],
            source=SYNTHETIC_SOURCE,
        )
    )

    vulnerability = model.add(
        Vulnerability(
            name='Unclassified Research Portal Weakness',
            description=(
                'Reported access weakness with a known high impact but insufficient '
                'technical detail to classify it or assign a CVSS score.'
            ),
            external_id='ARI-VULN-001',
            severity='High',
            # Insufficient technical evidence for a CVSS assessment.
            cvss_score=None,
            source=SYNTHETIC_SOURCE,
        )
    )

    loader = model.add(
        AttackTool(
            name='Horizon Loader',
            description=(
                'Fictional first-stage tool used to deploy the secondary collection '
                'component.'
            ),
            aliases=['Horizon Stage One'],
            tool_type='Loader',
            capabilities=['Deploy secondary tool'],
            source=SYNTHETIC_SOURCE,
        )
    )

    collector = model.add(
        AttackTool(
            name='Meridian Collector',
            description=(
                'Fictional second-stage tool used to collect confidential research '
                'documents.'
            ),
            aliases=['Meridian Stage Two'],
            tool_type='Collection Utility',
            capabilities=['Document collection'],
            source=SYNTHETIC_SOURCE,
        )
    )

    loader_instance = model.add(
        AttackToolInstance(
            name='Horizon Loader VM Instance',
            description=(
                'Simulated instance of Horizon Loader deployed to the research '
                'document VM.'
            ),
            observed_version='1.0.0',
            # SHA-256 of a synthetic label, not a real malware sample.
            hashes=['sha256:1a974049b6bd9af0fc03fd293845144073a08b7770bbba72ea5864135046cff2'],
            first_seen='2026-11-02',
            last_seen='2026-11-03',
            source=SYNTHETIC_SOURCE,
        )
    )

    collector_instance = model.add(
        AttackToolInstance(
            name='Meridian Collector VM Instance',
            description=(
                'Simulated instance of Meridian Collector deployed by the loader to '
                'the same VM.'
            ),
            observed_version='1.1.0',
            # SHA-256 of a synthetic label, not a real malware sample.
            hashes=['sha256:12fbc85ff2f4d75bcb32864ec4be311852c152cc0f0199cfa07954344469468d'],
            first_seen='2026-11-03',
            last_seen='2026-11-06',
            source=SYNTHETIC_SOURCE,
        )
    )

    # Organization relationships
    model.add(operatesIn(organization, sector))
    model.add(basedIn(organization, country))
    model.add(countryPartOf(country, international_body))

    # Infrastructure relationships
    model.add(manages(organization, infrastructure))
    model.add(madeBy(infrastructure, physical_hypervisor))
    model.add(madeBy(infrastructure, document_vm))
    model.add(runs(physical_hypervisor, document_vm))
    model.add(usedBy(infrastructure, researcher))
    model.add(hasAccessTo(researcher, document_vm))
    model.add(runsApp(document_vm, research_portal_instance))
    model.add(applicationInstanceOf(research_portal_instance, research_portal))
    model.add(applicationImplementsCode(research_portal_instance, document_viewer))
    model.add(launches(researcher, document_viewer))
    model.add(accessesInformation(document_viewer, research_results))
    model.add(userAccessesInformation(researcher, research_results))

    # CyberThreat relationships
    model.add(aliasOf(threat_actor_alias, threat_actor))
    model.add(initiates(threat_actor, threat))
    model.add(threatPartOf(threat, campaign))
    model.add(focusesOnCountry(campaign, country))
    model.add(targetsInternationalBody(campaign, international_body))
    model.add(targetsSector(campaign, sector))
    model.add(startsWith(threat, portal_compromise_step))
    model.add(followedBy(portal_compromise_step, document_collection_step))
    model.add(exploits(portal_compromise_step, vulnerability))
    model.add(employsTool(portal_compromise_step, loader_instance))
    model.add(employsTool(document_collection_step, collector_instance))
    model.add(deploysTool(loader_instance, collector_instance))
    model.add(toolInstanceOf(loader_instance, loader))
    model.add(toolInstanceOf(collector_instance, collector))
    model.add(deployedTo(loader_instance, document_vm))
    model.add(deployedTo(collector_instance, document_vm))

    return model


def main() -> None:
    """Run the fifth case study and print its validation outcome."""
    model = build_model()
    report = model.validate()

    print("Case Study 5")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
