import pytest

from metamodel.infrastructure.entities.Node import Node

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