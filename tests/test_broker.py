from broker import broker
from broker.providers import test_provider


def test_empty_init():
    """VMBroker should be able to init without any arguments"""
    broker_inst = broker.VMBroker()
    assert isinstance(broker_inst, broker.VMBroker)


def test_kwarg_assignment():
    """VMBroker should copy all kwargs into its _kwargs attribute"""
    broker_kwargs = {"test": "value", "another": 17}
    broker_inst = broker.VMBroker(**broker_kwargs)
    assert broker_inst._kwargs == broker_kwargs


def test_full_init():
    """Make sure all init checks and assignments work"""
    broker_hosts = ["test1.example.com", "test2.example.com", "test3.example.com"]
    broker_inst = broker.VMBroker(
        hosts=broker_hosts,
        test_action="blank",
        nick="test_nick"
    )
    assert broker_inst._hosts == broker_hosts
    assert not broker_inst._kwargs.get("hosts")
    assert broker_inst._provider_actions == {
        "test_action": (test_provider.TestProvider, "test_action")}
    assert not broker_inst._kwargs.get("nick")
    assert broker_inst._kwargs["test_action"] == "blank"


def test_broker_e2e():
    """Run through the base functionality of broker"""
    broker_inst = broker.VMBroker(nick="test_nick")
    broker_inst.checkout()
    assert len(broker_inst._hosts) == 1
    broker_host = broker_inst._hosts[0]
    assert broker_host.hostname == "test.host.example.com"
    broker_host_dict = broker_host.to_dict()
    assert broker_host_dict["_broker_provider"] == "TestProvider"
    broker_inst.checkin()
    assert len(broker_inst._hosts) == 0
