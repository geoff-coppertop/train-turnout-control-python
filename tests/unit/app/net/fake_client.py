#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# fake_client.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

class FakeClient(object):
    """
    """

    def __init__(self):
        """
        """
        self.__logger = logging.getLogger('fake_client')

        self.__is_running = False

    def start(self, connected_cb, disconnected_cb, data_rx_cb):
        self.__logger.debug('Starting client')

        self.connected = connected_cb
        self.disconnected = disconnected_cb

        self.__data_rx_cb = data_rx_cb

        self.__is_running = True

    def stop(self):
        self.__logger.debug('Stopping client')

        self.__is_running = False

    def is_running(self):
        return self.__is_running

    def send(self, data, length):
        self.__logger.debug('Sending data back')

        self.__data_rx_cb(data, length)
