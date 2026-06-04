"""Minimal infrastructure scenario for the CTI Feasibility Metamodel."""

from metamodel.core.Model import Model
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType
from metamodel.infrastructure.entities.Port import Port
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.UserType import UserType
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.OS import OS
from metamodel.infrastructure.entities.OSInstance import OSInstance
from metamodel.infrastructure.rels.hasNodeType import hasNodeType
from metamodel.infrastructure.rels.exposesPort import exposesPort
from metamodel.infrastructure.rels.hasUserType import hasUserType
from metamodel.infrastructure.rels.runsApplication import runsApplication
from metamodel.infrastructure.rels.applicationInstanceOf import applicationInstanceOf
from metamodel.infrastructure.rels.runsOs import runsOs
from metamodel.infrastructure.rels.osInstanceOf import osInstanceOf


def main() -> None:
    model = Model()

    node = model.add_entity(
        Node(
            name="web-server-01",
            hostname="web-server-01.example.local",
            ip_addresses=["10.0.0.10"],
            exposure="internet_facing",
        )
    )
    node_type = model.add_entity(NodeType(name="Server", taxonomy_ref="nodeTypes:server"))
    port = model.add_entity(Port(name="HTTPS", number=443, protocol="tcp", state="open"))
    user = model.add_entity(User(name="Alice Admin", username="alice", privilege_level="admin", mfa_enabled=True))
    user_type = model.add_entity(UserType(name="Administrator", taxonomy_ref="userTypes:administrator"))
    application = model.add_entity(Application(name="Nginx", vendor="F5", product="Nginx", version="1.24"))
    application_instance = model.add_entity(ApplicationInstance(name="Nginx on web-server-01", version="1.24"))
    os = model.add_entity(OS(name="Ubuntu Server", vendor="Canonical", product="Ubuntu", version="22.04"))
    os_instance = model.add_entity(OSInstance(name="Ubuntu Server on web-server-01", version="22.04", patch_level="current"))

    model.add_relationship(hasNodeType(node, node_type))
    model.add_relationship(exposesPort(node, port))
    model.add_relationship(hasUserType(user, user_type))
    model.add_relationship(runsApplication(node, application_instance))
    model.add_relationship(applicationInstanceOf(application_instance, application))
    model.add_relationship(runsOs(node, os_instance))
    model.add_relationship(osInstanceOf(os_instance, os))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")


if __name__ == "__main__":
    main()
