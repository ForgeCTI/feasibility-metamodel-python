"""Minimal cyber-threat scenario for the CTI Feasibility Metamodel."""

from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.threatPartOf import threatPartOf
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.employsTool import employsTool
from metamodel.cyberThreat.rels.toolInstanceOf import toolInstanceOf


def main() -> None:
    model = Model()

    actor = model.add(ThreatActor(name="Example threat actor", sophistication="high"))
    campaign = model.add(Campaign(name="Example phishing campaign", status="observed"))
    threat = model.add(Threat(name="Credential theft threat", objective="credential_access"))
    step = model.add(ThreatStep(name="Exploit public-facing application", sequence_index=1, phase="initial_access"))
    ttp = model.add(TTP(name="Exploit Public-Facing Application", taxonomy_ref="mitreAttackEnterprise:T1190"))
    vulnerability = model.add(SoftwareVulnerability(name="Example CVE", cve_id="CVE-2099-0001", cvss_score=8.8))
    tool = model.add(AttackTool(name="Example exploit kit", tool_type="exploit_kit"))
    tool_instance = model.add(AttackToolInstance(name="Exploit kit observed in campaign"))

    model.add(initiates(actor, threat))
    model.add(threatPartOf(threat, campaign))
    model.add(startsWith(threat, step))
    model.add(implementsTTP(step, ttp))
    model.add(exploits(step, vulnerability))
    model.add(employsTool(step, tool_instance))
    model.add(toolInstanceOf(tool_instance, tool))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")


if __name__ == "__main__":
    main()
