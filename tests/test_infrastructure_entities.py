import pytest

from metamodel.core.Model import Model
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.rels.runs import runs


# Node tests


@pytest.mark.parametrize(
    "address",
    [
        "192.168.1.10",
        "10.0.0.1",
        "2001:db8::1",
        "::1",
    ],
)
def test_node_accepts_valid_ip_addresses(address):
    node = Node(name="Server", ip_addresses=[address])
    assert node.ip_addresses == [address]


@pytest.mark.parametrize(
    "address",
    [
        "999.999.999.999",
        "192.168.1",
        "2001:db8::zz",
        "not-an-ip",
    ],
)
def test_node_rejects_invalid_ip_addresses(address):
    with pytest.raises(ValueError):
        Node(name="Server", ip_addresses=[address])


@pytest.mark.parametrize(
    "address",
    [
        "00:1A:2B:3C:4D:5E",
        "00:1a:2b:3c:4d:5e",
        "00:1a:2B:3c:4D:5e",
        "00-1A-2B-3C-4D-5E",
    ],
)
def test_node_accepts_valid_mac_addresses(address):
    node = Node(name="Server", mac_addresses=[address])
    assert node.mac_addresses == [address]


@pytest.mark.parametrize(
    "address",
    [
        "00:1A:2B:3C:4D",
        "00:1A:2B:3C:4D:ZZ",
        "00:1A-2B:3C-4D:5E",
        "invalid-mac",
    ],
)
def test_node_rejects_invalid_mac_addresses(address):
    with pytest.raises(ValueError):
        Node(name="Server", mac_addresses=[address])


def test_node_address_getters_return_copies():
    node = Node(
        name="Server",
        ip_addresses=["192.168.1.10"],
        mac_addresses=["00:1A:2B:3C:4D:5E"],
    )

    node.ip_addresses.append("999.999.999.999")
    node.mac_addresses.append("invalid-mac")

    assert node.ip_addresses == ["192.168.1.10"]
    assert node.mac_addresses == ["00:1A:2B:3C:4D:5E"]


def test_node_validates_address_assignments():
    node = Node(name="Server")

    with pytest.raises(ValueError):
        node.ip_addresses = ["999.999.999.999"]

    with pytest.raises(ValueError):
        node.mac_addresses = ["invalid-mac"]

    assert node.ip_addresses == []
    assert node.mac_addresses == []


# runs tests


def test_runs_allows_one_host_and_multiple_virtual_nodes():
    model = Model()
    host = model.add(Node(name="Physical Server"))
    vm1 = model.add(Node(name="Virtual Machine 1"))
    vm2 = model.add(Node(name="Virtual Machine 2"))
    model.add(Node(name="Standalone Server"))

    model.add(runs(host, vm1))
    model.add(runs(host, vm2))

    assert model.validate().is_valid


def test_runs_rejects_multiple_hosts_for_same_node():
    model = Model()
    host1 = model.add(Node(name="Physical Server 1"))
    host2 = model.add(Node(name="Physical Server 2"))
    vm = model.add(Node(name="Virtual Machine"))

    model.add(runs(host1, vm))
    model.add(runs(host2, vm))

    report = model.validate()

    assert not report.is_valid
    assert len(report.errors) == 1
    assert report.errors[0].validator == "cardinalityValidator"