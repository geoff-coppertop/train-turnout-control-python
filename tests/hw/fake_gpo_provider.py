#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# fake_gpo_provider.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
from src.hw.gpio.gpo_provider import GPOProvider

class FakeGPOProvider(GPOProvider):
    """GPO provider test double"""

    def __init__(self):
        """Create a GPO provider test double"""
        self.__logger = logging.getLogger('fake_gpo_provider')

        self.__is_enabled = False

    def enable(self):
        """Enable output"""
        self.__is_enabled = True

    def disable(self):
        """Disable output"""
        self.__is_enabled = False

    def is_enabled(self):
        """Return output status"""
        return self.__is_enabled

