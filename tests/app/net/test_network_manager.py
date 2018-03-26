#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test_network_manager.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import pytest
import time

from src.app.net.network_manager import NetworkManager

from tests.app.net.fake_client import FakeClient
from tests.app.net.fake_server import FakeServer

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture
def client():
    """Create a fake client object"""
    return FakeClient()

@pytest.fixture
def server():
    """Create a fake server object"""
    return FakeServer()

@pytest.fixture(name='s_endp')
def single_endpoint(mocker):
    """Create a single network manager endpoint mock"""
    return mocker.stub()

@pytest.fixture(name='m_endp')
def multi_endpoint(mocker):
    """Create a multi network manager endpoint mock"""
    return [mocker.stub(), mocker.stub()]

@pytest.fixture(name='nm_client_only')
def nm_client_only(s_endp, client):
    """Create a client only network manager"""
    return NetworkManager(s_endp, client, discovery_timeout=0.1, randomize_timeout=False)

@pytest.fixture(name='nm_client_server')
def nm_client_server(s_endp, client, server):
    """Create a client-server network manager"""
    return NetworkManager(s_endp, client=client, server=server, discovery_timeout=0.1, randomize_timeout=False)

#-------------------------------------------------------------------------------
# Init tests
#-------------------------------------------------------------------------------
def test_invalid_client_init(s_endp):
    """Ensure that initialization with an invalid client fails"""
    with pytest.raises(AttributeError):
        NetworkManager(s_endp, None)

def test_client_invalid_endpoint_init(client):
    """Check that initialization with an invalid endpoint fails"""
    with pytest.raises(AttributeError):
        NetworkManager(None, client, discovery_timeout=0.1, randomize_timeout=False)

def test_discovery_timeout_randomizer(s_endp, client):
    """Check that discovery timeout randomizer falls within limits"""
    net_man = NetworkManager(s_endp, client)

    assert net_man.discovery_timeout in range(
            int(NetworkManager.DISCOVERY_TIMEOUT_S * (1 - NetworkManager.DISCOVERY_TIMEOUT_RAND_FACTOR)),
            int(NetworkManager.DISCOVERY_TIMEOUT_S * (1 + NetworkManager.DISCOVERY_TIMEOUT_RAND_FACTOR)))

#-------------------------------------------------------------------------------
# Client only tests
#-------------------------------------------------------------------------------
def test_co_search_sub_timeout(nm_client_only, client, server):
    """Test that a client only implementation does not try and start a server"""
    nm_client_only.search()
    time.sleep(nm_client_only.discovery_timeout - 0.05)
    assert 'searching' == nm_client_only.state
    assert client.is_running()
    assert not server.is_running()

def test_co_search_timeout(nm_client_only, client, server):
    """Test etwork manager stays in search state after discovery timeout"""
    nm_client_only.search()
    time.sleep(nm_client_only.discovery_timeout + 0.05)
    assert 'searching' == nm_client_only.state
    assert client.is_running()
    assert not server.is_running()

#-------------------------------------------------------------------------------
# Client-Server tests
#-------------------------------------------------------------------------------
def test_cs_startup_to_init(nm_client_server, client, server):
    """Test a C/S network manager starts in the initializing state"""
    assert 'initializing' == nm_client_server.state
    assert not client.is_running()
    assert not server.is_running()

def test_cs_startup_shutdown(nm_client_server, client, server):
    """Show that calling shutdown from the initialized state is safe"""
    nm_client_server.shutdown()
    assert 'initializing' == nm_client_server.state
    assert not client.is_running()
    assert not server.is_running()

def test_cs_search_start(nm_client_server, client, server):
    """Show that we search with client first"""
    nm_client_server.search()
    assert 'searching' == nm_client_server.state
    assert client.is_running()
    assert not server.is_running()

def test_cs_search_sub_timeout(nm_client_server, client, server):
    """Client is searching until discovery timeout elapses"""
    nm_client_server.search()
    time.sleep(nm_client_server.discovery_timeout - 0.05)
    assert 'searching' == nm_client_server.state
    assert client.is_running()
    assert not server.is_running()

def test_cs_search_timeout(nm_client_server, client, server):
    """Server is searching after discovery timeout"""
    nm_client_server.search()
    time.sleep(nm_client_server.discovery_timeout + 0.05)
    assert 'searching' == nm_client_server.state
    assert server.is_running()
    assert not client.is_running()

def test_cs_connected_client_sub_timeout(nm_client_server, client, server):
    """C/S netowrk manager will go to connected state with client connection"""
    nm_client_server.search()
    client.connected()
    assert 'connected' == nm_client_server.state

def test_cs_connected_client_timeout(nm_client_server, client, server):
    """Discovery timeout has no effect once client connected"""
    nm_client_server.search()
    client.connected()
    time.sleep(nm_client_server.discovery_timeout + 0.05)
    assert client.is_running()
    assert not server.is_running()

def test_cs_connected_server(nm_client_server, client, server):
    """C/S netowrk manager will go to connected state with server connection"""
    nm_client_server.search()
    time.sleep(nm_client_server.discovery_timeout + 0.05)
    server.connected()
    assert 'connected' == nm_client_server.state
    assert not client.is_running()
    assert server.is_running()

def test_cs_connected_client_disconnect(nm_client_server, client, server):
    """C/S network manager will go back to client search"""
    nm_client_server.search()
    client.connected()
    client.disconnected()
    assert client.is_running()
    assert not server.is_running()
    assert 'searching' == nm_client_server.state

def test_cs_connected_server_disconnect(nm_client_server, client, server):
    """C/S network manager will go back to client search"""
    nm_client_server.search()
    time.sleep(nm_client_server.discovery_timeout + 0.05)
    server.connected()
    server.disconnected()
    assert client.is_running()
    assert not server.is_running()
    assert 'searching' == nm_client_server.state

#-------------------------------------------------------------------------------
# Communication tests
#-------------------------------------------------------------------------------
def test_send_during_search(s_endp, client):
    net_man = NetworkManager(s_endp, client, discovery_timeout=0.1, randomize_timeout=False)
    net_man.search()

    with pytest.raises(SystemError):
        net_man.send('Test', 4)

def test_client_transmission(s_endp, client):
    """Check end to end client communication"""
    net_man = NetworkManager(s_endp, client, discovery_timeout=0.1, randomize_timeout=False)
    net_man.search()

    client.connected()

    net_man.send('Test', 4)

    s_endp.assert_called_once_with('Test', 4)

def test_client_multi_endpoint_transmission(m_endp, client):
    """Check end to end client communication to multiple endpoints"""
    net_man = NetworkManager(m_endp, client, discovery_timeout=0.1, randomize_timeout=False)
    net_man.search()

    client.connected()

    net_man.send('Test', 4)

    for endpoint in m_endp:
        endpoint.assert_called_once_with('Test', 4)

def test_server_transmission(s_endp, client, server):
    """Check end to end server communication"""
    net_man = NetworkManager(s_endp, client, server, discovery_timeout=0.1, randomize_timeout=False)
    net_man.search()

    time.sleep(net_man.discovery_timeout + 0.05)
    server.connected()

    net_man.send('Test', 4)

    s_endp.assert_called_once_with('Test', 4)
