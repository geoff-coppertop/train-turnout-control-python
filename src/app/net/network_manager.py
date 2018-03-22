#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# network_manager.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import random

from transitions.extensions import LockedMachine as Machine
from transitions.extensions.states import add_state_features, Timeout

@add_state_features(Timeout)
class NetworkManager(Machine):
    """Object for managing network resources for the node"""

    DISCOVERY_TIMEOUT_S =           10
    DISCOVERY_TIMEOUT_RAND_FACTOR = 0.25

    def __init__(
        self,
        endpoints,
        client,
        server=None,
        discovery_timeout=DISCOVERY_TIMEOUT_S,
        randomize_timeout=True):
        """Create a network manager"""
        self.__logger = logging.getLogger('network_manager')

        if randomize_timeout:
            self.discovery_timeout = random.randint(
                int(discovery_timeout * (1 - NetworkManager.DISCOVERY_TIMEOUT_RAND_FACTOR)),
                int(discovery_timeout * (1 + NetworkManager.DISCOVERY_TIMEOUT_RAND_FACTOR)))
        else:
            self.discovery_timeout = discovery_timeout

        self.__STATES = [
            { 'name': 'initializing',
                'on_enter':     '_stop' },
            { 'name': 'searching',
                'timeout':      self.discovery_timeout,
                'on_timeout':   '_start_server',
                'on_enter':     '_start_client' },
            { 'name': 'connected' },
        ]

        self.__TRANSITIONS = [
            { 'trigger': 'search',          'source': 'initializing',   'dest': 'searching' },
            { 'trigger': 'connected',       'source': 'searching',     'dest': 'connected' },
            { 'trigger': 'disconnected',    'source': 'connected',      'dest': 'searching' },
            { 'trigger': 'shutdown',        'source': '*',              'dest': 'initializing' }
        ]

        Machine.__init__(
            self,
            states=self.__STATES,
            transitions=self.__TRANSITIONS,
            initial='initializing',
            auto_transitions=False)

        # Required to provide a client
        if None == client:
            raise AttributeError('Client must be specified')

        self.__roles = {
            'client': client,
            'server': server }

        self.__role = 'client'

        if type(endpoints) is not list:
            self.__endpoints = [endpoints]
        else:
            self.__endpoints = endpoints

        self.__endpoints = [endp for endp in self.__endpoints if endp is not None]

        if not len(self.__endpoints):
            raise AttributeError('No endpoints specified')

    def send(self, data, length):
        """Send data using active role"""
        if self.state is not 'connected':
            raise SystemError('System must be connected to send data')

        self.__logger.debug('Sending data')

        self.__get_role().send(data, length)

    def _stop(self):
        """Stop all roles"""
        for role in self.__roles:
            role_to_stop = self.__roles[role]

            if (role_to_stop is not None) and role_to_stop.is_running():
                role_to_stop.stop()

    def _start_client(self):
        """Start the client role"""
        self.__start_role('client')

    def _start_server(self):
        """Start the server role if available"""
        if self.__roles['server'] is not None:
            self.__start_role('server')
        else:
            raise RuntimeError('No server to start')

    def __get_role(self):
        """Get the current role"""
        return self.__roles[self.__role]

    def __start_role(self, new_role):
        """Start a given role"""

        # Start by stopping all roles, this might be too much if a node can
        # have dual roles
        self._stop()

        # Set the new role
        self.__role = new_role

        # Start the new role
        self.__get_role().start(self.connected, self.disconnected, self.__data_rx)

    def __data_rx(self, data, length):
        """Call all endpoints with received data"""
        for endpoint in self.__endpoints:
            endpoint(data, length)

