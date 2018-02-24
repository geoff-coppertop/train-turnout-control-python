#!/usr/bin/env python
# # -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# gpo_provider.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

class GPOProvider(object):
    """Provides a general purpose output interface"""

    def __init__(self):
        """Create a GPO object"""
        raise NotImplementedError(
            "You're trying to instantiate an an abstract GPO provider.")

    def enable(self):
        """Turn on the output"""
        raise NotImplementedError(
            "You're trying to use an abstract method to enable the output.")

    def disable(self):
        """Turn off the output"""
        raise NotImplementedError(
            "You're trying to use an abstract method to disable the output.")