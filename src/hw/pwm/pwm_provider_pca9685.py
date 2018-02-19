#!/usr/bin/env python
# # -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# pwm_provider_pca9685.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

from pwm_provider import PWM_Provider

class PWM_Provider_PCA9685(PWM_Provider):
    """Concrete definition of a PWM provider that use the PCA9685"""

    MIN_FREQ = 24
    MAX_FREQ = 1526

    MIN_PIN = 0
    MAX_PIN = 15

    def __init__(self, device, pin):
        """Creates a PWM provider

        Uses a PCA9685 device and the desired pin on that device
        """
        self.__logger = logging.getLogger('hw.pwm.pwm-provider-pca9685')
        self.__dev = device
        self.__pin = pin

        self.__logger.info('PCA9685 PWM provider created')
        self.__logger.info('Pin: %d', pin)

        assert(self.__pin >= self.MIN_PIN)
        assert(self.__pin <= self.MAX_PIN)

        super(PWM_Provider_PCA9685, self).__init__(self.MIN_FREQ, self.MAX_FREQ)

    def set_duty(self, duty):
        """Sets the duty cycle of the pin specified by the PWM provider.

        Duty cycle is expressed as a percentage.
        """
        self.__logger.info('Requested duty: %d', duty)

        # TODO: these checks should probably be moved to the base class
        # Check that the duty cycle requested is valid
        assert(duty >= self._min_duty)
        assert(duty <= self._max_duty)

        self.__logger.info('Limited duty: %d', duty)

        # Scale duty to send it to the PCA9685
        duty = int(duty * 0x0FFF / 100)

        self.__logger.info('Scaled duty: %d', duty)

        PWM_Provider.set_duty(self, duty)

    def set_freq(self, freq):
        """Set PWM frequency for the PWM provider.

        For the PCA9685 this affects all pins simulatneously.
        """
        self.__logger.info('Current freq: %d', self.__dev.get_pwm_frequency())
        self.__logger.info('Requested freq: %d', freq)

        # TODO: these checks should probably be moved to the base class
        # Check that the freq requested is valid
        assert(freq > self._min_freq)
        assert(freq < self._max_duty)

        if(freq == self.__dev.get_pwm_frequency()):
            return

        self.__dev.set_pwm_frequency(freq)

    def turn_on(self):
        """Turn on the PWM provider at the set duty cycle"""
        self.__dev.set_pwm(self.__pin, self._duty)

    def turn_off(self):
        """Turn off the PWM provider"""
        self.__dev.set_pwm(self.__pin, 0)

