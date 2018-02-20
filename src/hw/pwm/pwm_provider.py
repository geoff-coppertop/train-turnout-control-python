#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------
pwm-provider.py
--------------------------------------------------------------------------------
Class definition to abstract PWM generation
--------------------------------------------------------------------------------
"""

import logging

class PWMProvider(object):
    def __init__(self, min_freq, max_freq, min_duty=0, max_duty=100):
        """Create a PWM provider"""
        self.__logger = logging.getLogger('hw.pwm.pwm-provider')
        self._duty = 0
        self._min_duty = min_duty
        self._max_duty = max_duty
        self._min_freq = min_freq
        self._max_freq = max_freq

    def set_duty(self, duty):
        """Set the duty cycle of the PWM provider"""
        self.__logger.info('Duty Cycle: %d', duty)
        self._duty = duty

    def set_freq(self, freq):
        """Set the frequency of the PWM provider"""
        raise NotImplementedError("You're trying to use an abstract method to get frequency.")

    def turn_on(self):
        """Turn on the PWM provider at the set duty cycle"""
        raise NotImplementedError("You're trying to use an abstract method to turn the output on.")

    def turn_off(self):
        """Turn off the PWM provider"""
        raise NotImplementedError("You're trying to use an abstract method to turn the output off.")


