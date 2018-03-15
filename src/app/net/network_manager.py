#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# network_manager.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import socket
import uuid

from time import sleep
from transitions.extensions import LockedMachine as Machine
from transitions.extensions.states import add_state_features, Timeout

@add_state_features(Timeout)
class NetworkManager(Machine):
    """Object for managing network resources for the node"""

    DISCOVERY_TIMEOUT = 10

    TRANSITIONS = [
            { 'trigger': 'search',          'source': 'initializing',   'dest': 'searching' },
            { 'trigger': 'connected',       'source': 'searching',     'dest': 'connected' },
            { 'trigger': 'disconnected',    'source': 'connected',      'dest': 'searching' },
            { 'trigger': 'shutdown',        'source': '*',              'dest': 'initializing' }
        ]

    STATES = [
            { 'name': 'initializing',
                'on_enter':     '_stop' },
            { 'name': 'searching',
                'timeout':      DISCOVERY_TIMEOUT,
                'on_timeout':   '_start_server',
                'on_enter':     '_start_client' },
            { 'name': 'connected' },
        ]

    def __init__(self, client, server=None):
        """Create a network manager"""
        self.__logger = logging.getLogger('network_manager')

        Machine.__init__(
            self,
            states=NetworkManager.STATES,
            transitions=NetworkManager.TRANSITIONS,
            initial='initializing',
            auto_transitions=False)

        # Required to provide a client
        if None == client:
            raise AttributeError('Client must be specified')

        self.__roles = {
            'client': client,
            'server': server }

        self.__role = 'client'

    def send(self, data):
        self.__logger.debug('Sending data')

        self.__roles[self.__role].send(data)

    def _stop(self):
        for role in self.__roles:
            role_to_stop = self.__roles[role]

            if (role_to_stop is not None) and role_to_stop.is_running():
                role_to_stop.stop()

    def _start_client(self):
        self.__start_role('client')

    def _start_server(self):
        if self.__roles['server'] is not None:
            self.__start_role('server')
        else:
            raise RuntimeError('No server to start')

    def __start_role(self, new_role):
        if new_role.lower() not in self.__roles:
            raise AttributeError('Unable to start role: ' + new_role)

        curr_role = self.__roles[self.__role]

        if curr_role.is_running():
            curr_role.stop()

        self.__role = new_role

        self.__roles[self.__role].start(self.connected, self.disconnected)

