#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# gpo_provider_pwm.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
from gpo_provider import GPOProvider

class GPOProviderPWM(GPOProvider):
    """Concreate implementation of a GPO provider that uses a PWM provider
    """

    def __init__(self, pwm_provider):
        """Create a GPO provider that uses a PWM provider for output generation
        """
        self.__logger = logging.getLogger('gpo_provider_pwm')

        self.__pwm = pwm_provider
        self.__pwm.turn_off()
        self.__pwm.set_duty(100)

    def enable(self):
        """Turn on the output"""
        self.__logger.info('Output turned on.')

        self.__pwm.turn_on()

    def disable(self):
        """Turn off the output"""
        self.__logger.info('Output turned off.')

        self.__pwm.turn_off()


