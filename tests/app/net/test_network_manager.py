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

@pytest.fixture
def network_manager_client_only(client):
    """Create a client only network manager"""
    assert client is not None
    return NetworkManager(client)

@pytest.fixture
def network_manager_client_server(client, server):
    """Create a client-server network manager"""
    assert server is not None
    assert client is not None
    return NetworkManager(client=client, server=server)

#-------------------------------------------------------------------------------
# Client only tests
#-------------------------------------------------------------------------------
def test_co_search_sub_timeout(network_manager_client_only, client, server):
    """Test that a client only implementation does not try and start a server"""
    network_manager_client_only.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT - 0.01)
    assert 'searching' == network_manager_client_only.state
    assert client.is_running()
    assert not server.is_running()

def test_co_search_timeout(network_manager_client_only, client, server):
    network_manager_client_only.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT + 0.01)
    assert 'searching' == network_manager_client_only.state
    assert client.is_running()
    assert not server.is_running()

#-------------------------------------------------------------------------------
# Client-Server tests
#-------------------------------------------------------------------------------
def test_cs_startup_to_init(network_manager_client_server, client, server):
    assert 'initializing' == network_manager_client_server.state
    assert not client.is_running()
    assert not server.is_running()

def test_cs_startup_shutdown(network_manager_client_server, client, server):
    network_manager_client_server.shutdown()
    assert 'initializing' == network_manager_client_server.state
    assert not client.is_running()
    assert not server.is_running()

def test_cs_search_start(network_manager_client_server, client, server):
    network_manager_client_server.search()
    assert 'searching' == network_manager_client_server.state
    assert client.is_running()
    assert not server.is_running()

def test_cs_search_sub_timeout(network_manager_client_server, client, server):
    network_manager_client_server.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT - 0.01)
    assert 'searching' == network_manager_client_server.state
    assert client.is_running()
    assert not server.is_running()

def test_cs_search_timeout(network_manager_client_server, client, server):
    network_manager_client_server.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT + 0.01)
    assert 'searching' == network_manager_client_server.state
    assert server.is_running()
    assert not client.is_running()

def test_cs_connected_client_sub_timeout(network_manager_client_server, client, server):
    network_manager_client_server.search()
    client.connected()
    assert 'connected' == network_manager_client_server.state

def test_cs_connected_client_timeout(network_manager_client_server, client, server):
    network_manager_client_server.search()
    client.connected()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT + 0.01)
    assert client.is_running()
    assert not server.is_running()

def test_cs_connected_server(network_manager_client_server, client, server):
    network_manager_client_server.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT + 0.01)
    server.connected()
    assert 'connected' == network_manager_client_server.state
    assert not client.is_running()
    assert server.is_running()

def test_cs_connected_client_disconnect(network_manager_client_server, client, server):
    network_manager_client_server.search()
    client.connected()
    client.disconnected()
    assert client.is_running()
    assert not server.is_running()
    assert 'searching' == network_manager_client_server.state

def test_cs_connected_server_disconnect(network_manager_client_server, client, server):
    network_manager_client_server.search()
    time.sleep(NetworkManager.DISCOVERY_TIMEOUT + 0.01)
    server.connected()
    server.disconnected()
    assert client.is_running()
    assert not server.is_running()
    assert 'searching' == network_manager_client_server.state