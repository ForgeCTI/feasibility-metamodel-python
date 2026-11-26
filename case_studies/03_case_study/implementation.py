"""
Case Study 03 - Credential Phishing Campaign.

This case study models a fictional phishing campaign
targeting employees of a consulting company, "Bluehaven Consulting".

The scenario focuses on a threat actor, a phishing campaign,
the techniques employed, human vulnerabilities, and the
sequence of actions involved in credential theft.

The purpose is to demonstrate how entities and relationships
from the Organization, Infrastructure, and CyberThreat
submodels can be instantiated and combined to represent
a coherent attack scenario.
"""


from metamodel.core.Model import Model

# Organization entities
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector

# Infrastructure entities
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.UserType import UserType

# CyberThreat entities
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.HumanVulnerability import HumanVulnerability
from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.AdversaryType import AdversaryType
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration
from metamodel.cyberThreat.entities.Indicator import Indicator

# Organization relationships
from metamodel.organization.rels.operatesIn import operatesIn

# Infrastructure relationships
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.usedBy import usedBy
from metamodel.infrastructure.rels.hasUserType import hasUserType

# CyberThreat relationships
from metamodel.cyberThreat.rels.targetsSector import targetsSector
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.threatPartOf import threatPartOf
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.followedBy import followedBy
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP
from metamodel.cyberThreat.rels.affectsUser import affectsUser
from metamodel.cyberThreat.rels.relatedTo import relatedTo
from metamodel.cyberThreat.rels.hasAdversaryType import hasAdversaryType
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise
from metamodel.cyberThreat.rels.employsTool import employsTool
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf
from metamodel.cyberThreat.rels.hasConfig import hasConfig
from metamodel.cyberThreat.rels.requiresConfig import requiresConfig
from metamodel.cyberThreat.rels.requiresExpertise import requiresExpertise
from metamodel.cyberThreat.rels.producesIndicator import producesIndicator
from metamodel.cyberThreat.rels.associatedToTool import associatedToTool
from metamodel.cyberThreat.rels.exploits import exploits

def build_model() -> Model:
    """Build the fictional Bluehaven Consulting phishing scenario."""
    model = Model()

    organization = model.add(
        Organization(
            name="Bluehaven Consulting",
            description=(
                "Fictional management consultancy targeted "
                "by a credential phishing campaign."
            ),
            legal_name="Bluehaven Consulting S.r.l.",
            short_name="BC",
            website="https://bluehaven-consulting.example",
            organization_size="Medium",
            criticality="High",
            maturity_level="Intermediate",
            source="Synthetic case study data",
        )
    )

    sector = model.add(
        Sector(
            name="Management Consulting",
            description=(
                "Management advisory and business consulting services."
            ),
            sector_code="70.22",
            sector_standard="NACE",
            sector_standard_version="Rev. 2",
            source="Synthetic case study data",
        )
    )

    threat_actor = model.add(
        ThreatActor(
            name="Invoice Lure Group",
            description=(
                "Fictional threat actor conducting credential "
                "harvesting through phishing messages."
            ),
            aliases=["ILG"],
            motivation="Financial gain",
            sophistication="Moderate",
            country="Unknown",
            source="Synthetic case study data",
        )
    )

    phishing_campaign = model.add(
        Campaign(
            name="Consulting Sector Credential Phishing Campaign",
            description=(
                "Fictional phishing campaign targeting "
                "employees in the consulting sector."
            ),
            first_seen="2026-10-14",
            last_seen="2026-10-22",
            status="Completed",
            objective=(
                "Steal employee credentials through "
                "fraudulent login pages."
            ),
            source="Synthetic case study data",
        )
    )

    phishing_threat = model.add(
        Threat(
            name="Employee Credential Theft",
            description=(
                "Phishing threat seeking to compromise "
                "a consulting employee account."
            ),
            objective=(
                "Obtain employee login credentials "
                "for unauthorized access."
            ),
            first_seen="2026-10-15",
            last_seen="2026-10-21",
            source="Synthetic case study data",
        )
    )

    phishing_email_step = model.add(
        ThreatStep(
            name="Phishing Email Delivery",
            description=(
                "Delivery of a fraudulent business email containing "
                "a link to a fake corporate login page."
            ),
            phase="Initial Access",
            objective=(
                "Direct a Bluehaven employee to a fraudulent login page."
            ),
            preconditions=[
                "A target employee email address is known."
            ],
            postconditions=[
                "A phishing email containing the deceptive link has been delivered."
            ],
            source="Synthetic case study data",
        )
    )

    credential_capture_step = model.add(
        ThreatStep(
            name="Credential Capture",
            description=(
                "An employee follows the phishing link and enters "
                "credentials into the fraudulent login page."
            ),
            phase="Credential Access",
            objective="Capture the employee login credentials.",
            preconditions=[
                "The phishing message has been delivered to the employee."
            ],
            postconditions=[
                "The attacker has obtained the submitted credentials."
            ],
            source="Synthetic case study data",
        )
    )

    phishing_ttp = model.add(
        TTP(
            name="Spearphishing Link",
            description=(
                "Social-engineering delivery of a malicious "
                "link through email."
            ),
            external_id="T1566.002",
            tactic="Initial Access",
            technique="Phishing",
            subtechnique="Spearphishing Link",
            source="MITRE ATT&CK (scenario mapping)",
        )
    )

    credential_capture_ttp = model.add(
        TTP(
            name="Web Portal Capture",
            description=(
                "Capture of credentials submitted "
                "through a deceptive login portal."
            ),
            external_id="T1056.003",
            tactic="Credential Access",
            technique="Input Capture",
            subtechnique="Web Portal Capture",
            source="MITRE ATT&CK (scenario mapping)",
        )
    )

    corporate_infrastructure = model.add(
        Infrastructure(
            name="Bluehaven Corporate IT Infrastructure",
            description=(
                "Corporate infrastructure supporting employee "
                "email services and authentication."
            ),
            environment_type="Production",
            scope="Corporate email and employee authentication",
            source="Synthetic case study data",
        )
    )

    target_employee = model.add(
        User(
            name="Bluehaven Consulting Employee",
            description=(
                "Employee account targeted by the phishing "
                "campaign through a fraudulent login page."
            ),
            username="m.rossi",
            email="m.rossi@bluehaven-consulting.example",
            role="Business Consultant",
            mfa_enabled=False,
            source="Synthetic case study data",
        )
    )

    employee_user_type = model.add(
        UserType(
            name="Consulting Staff",
            description=(
                "Standard employee accounts used by "
                "Bluehaven Consulting personnel."
            ),
            privilege_level="Standard",
            source="Synthetic case study data",
        )
    )

    phishing_susceptibility = model.add(
        HumanVulnerability(
            name="Phishing Susceptibility",
            description=(
                "Susceptibility to deceptive messages "
                "impersonating legitimate corporate services."
            ),
            vulnerability_type="Social Engineering",
            severity="High",
            external_id=None,
            cvss_score=None,
            source="Synthetic case study data",
        )
    )

    phishing_adversary = model.add(
        Adversary(
            name="Credential Phishing Adversary",
            description=(
                "Adversarial profile associated with financially "
                "motivated credential phishing operations."
            ),
            objective=(
                "Obtain corporate credentials for unauthorized "
                "account access and potential financial gain."
            ),
            capability_level="Moderate",
            source="Synthetic case study data",
        )
    )

    cybercriminal_type = model.add(
        AdversaryType(
            name="Financially Motivated Cybercriminal",
            description=(
                "Adversary category characterized by attacks "
                "conducted primarily for financial gain."
            ),
            category="Cybercriminal",
            source="Synthetic case study data",
        )
    )

    phishing_expertise = model.add(
        Expertise(
            name="Credential Phishing Expertise",
            description=(
                "Skills required to conduct phishing campaigns "
                "using social engineering and deceptive login pages."
            ),
            level="Intermediate",
            domain="Social Engineering and Credential Theft",
            source="Synthetic case study data",
        )
    )

    phishing_tool = model.add(
        AttackTool(
            name="Credential Phishing Web Kit",
            description=(
                "Fictional phishing tool used to imitate "
                "corporate authentication portals."
            ),
            aliases=["Corporate Login Clone Kit"],
            tool_type="Phishing Kit",
            capabilities=[
                "Login page impersonation",
                "Credential collection",
            ],
            source="Synthetic case study data",
        )
    )

    phishing_tool_instance = model.add(
        AttackToolInstance(
            name="Bluehaven Fake Login Portal Instance",
            description=(
                "Specific phishing tool instance associated "
                "with the credential capture phase."
            ),
            observed_version="1.0",
            hashes=[
                "sha256:9d9b3aadb3a2d31e47cf9922b269157f3431dbda0e2c05b8671fa877739e7cda"
            ],
            first_seen="2026-10-15",
            last_seen="2026-10-21",
            source="Synthetic case study data",
        )
    )

    phishing_tool_configuration = model.add(
        AttackToolConfiguration(
            name="Bluehaven Portal Configuration",
            description=(
                "Fictional configuration associated with "
                "the simulated corporate login portal."
            ),
            configuration_type="Phishing Portal Configuration",
            parameters={
                "portal_theme": "Corporate SSO imitation",
                "collection_mode": "Simulated",
            },
            persistence_enabled=False,
            stealth_level="Low",
            source="Synthetic case study data",
        )
    )

    phishing_domain_indicator = model.add(
        Indicator(
            name="Fake Bluehaven Login Domain",
            description=(
                "Domain associated with the fraudulent login "
                "portal used in the credential phishing campaign."
            ),
            indicator_type="domain-name",
            value="bluehaven-sso-login.example",
            pattern=(
                "[domain-name:value = "
                "'bluehaven-sso-login.example']"
            ),
            valid_from="2026-10-15",
            valid_until="2026-10-21",
            source="Synthetic case study data",
        )
    )

    model.add(operatesIn(organization, sector))
    model.add(targetsSector(phishing_campaign, sector))
    model.add(initiates(threat_actor, phishing_threat))
    model.add(threatPartOf(phishing_threat, phishing_campaign))
    model.add(startsWith(phishing_threat, phishing_email_step))
    model.add(followedBy(phishing_email_step, credential_capture_step))
    model.add(implementsTTP(phishing_email_step, phishing_ttp))
    model.add(implementsTTP(credential_capture_step, credential_capture_ttp))
    model.add(manages(organization, corporate_infrastructure))
    model.add(usedBy(corporate_infrastructure, target_employee))
    model.add(hasUserType(target_employee, employee_user_type))
    model.add(affectsUser(phishing_susceptibility, target_employee))
    model.add(relatedTo(threat_actor, phishing_adversary))
    model.add(hasAdversaryType(phishing_adversary, cybercriminal_type))
    model.add(hasExpertise(threat_actor, phishing_expertise))
    model.add(employsTool(credential_capture_step, phishing_tool_instance))
    model.add(toolInstanceOf(phishing_tool_instance, phishing_tool))
    model.add(hasConfig(phishing_tool_instance, phishing_tool_configuration))
    model.add(requiresConfig(phishing_tool, phishing_tool_configuration))
    model.add(requiresExpertise(phishing_tool, phishing_expertise))
    model.add(producesIndicator(phishing_tool_instance, phishing_domain_indicator))
    model.add(associatedToTool(phishing_domain_indicator, phishing_tool_instance))
    model.add(exploits(credential_capture_step, phishing_susceptibility))

    return model


def main() -> None:
    """Run the case-study implementation."""
    model = build_model()
    report = model.validate()

    print("Case Study 3")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
