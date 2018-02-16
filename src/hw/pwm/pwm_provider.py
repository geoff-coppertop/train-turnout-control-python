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

class PWM_Provider(object):
    def __init__(self):
        """
        Create a PWM provider
        """
        self.__logger = logging.getLogger('hw.pwm.pwm-provider')
        self.__duty = 0

    def set_duty(self, duty):
        """
        Set the duty cycle of the PWM provider
        """
        self.__logger.info('Duty Cycle: %d', duty)
        self.__duty = duty

    def set_freq(self, freq):
        """
        Set the frequency of the PWM provider
        """
        raise NotImplementedError("You're trying to use an abstract method to get frequency.")

    def turn_on(self):
        """
        Turn on the PWM provider at the set duty cycle
        """
        raise NotImplementedError("You're trying to use an abstract method to turn the output on.")

    def turn_off(self):
        """
        Turn off the PWM provider
        """
        raise NotImplementedError("You're trying to use an abstract method to turn the output off.")


