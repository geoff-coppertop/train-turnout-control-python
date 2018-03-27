#!/usr/bin/env python
# # -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# fake_pwm_provider.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import time

from src.hw.pwm.pwm_provider import PWMProvider

class FakePWMProvider(PWMProvider):
    """
    """

    def __init__(self):
        """
        """
        self.__logger = logging.getLogger('fake_pwm_provider')
        self.__freq = 0
        self.__duty = 0
        self.__on_count = 0
        self.__output_enabled = False

    def get_duty(self):
        """Return the current duty cycle"""
        return self.__duty

    def set_duty(self, duty):
        """Set the duty cycle of the PWM provider"""
        self.__logger.info('Duty Cycle: %d', duty)
        self.__duty = duty

    def get_freq(self):
        """Return the current frequency"""
        return self.__freq

    def set_freq(self, freq):
        """Set the frequency of the PWM provider"""
        self.__freq = freq

    def turn_on(self):
        """Turn on the PWM provider at the set duty cycle"""
        self.__on_count += 1
        self.__output_enabled = True

    def turn_off(self):
        """Turn off the PWM provider"""
        self.__output_enabled = False

    def get_on_count(self):
        return self.__on_count

    def output_enabled(self):
        return self.__output_enabled