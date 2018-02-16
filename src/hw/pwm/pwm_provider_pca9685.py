#!/usr/bin/env python
# # -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------
pwm_provider_pca9685.py
--------------------------------------------------------------------------------
Concrete definition of a PWM provider that use the PCA9685
--------------------------------------------------------------------------------
"""

import logging

from pwm_provider import PWM_Provider
from pca9685_driver import Device

class PWM_Provider_PCA9685(PWM_Provider):
    def __init__(self, device, pin):
        """
        Creates a PWM provider given a PCA9685 device and the desired pin on
        that device
        """
        self.__logger = logging.getLogger('hw.pwm.pwm-provider-pca9685')
        self.__dev = device
        self.__pin = pin

        self.__logger.info('PCA9685 PWM provider created')
        self.__logger.info('Pin: %d', pin)

    def set_duty(self, duty):
        """
        Sets the duty cycle of the pin specified by the PWM provider.
        Duty cycle is expressed as a percentage.
        """
        self.__logger.info('Requested duty: %d', duty)

        # Limit the duty cycle
        duty = max(duty, 0)
        duty = min(duty, 100)

        self.__logger.info('Limited duty: %d', duty)

        # Scale duty to send it to the PCA9685
        duty = int(duty * 0x0FFF / 100)

        self.__logger.info('Scaled duty: %d', duty)

        PWM_Provider.set_duty(self, duty)

    def set_freq(self, freq):
        """
        Set PWM frequency for the PWM provider.
        For the PCA9685 this affects all pins simulatneously.
        """
        self.__logger.info('Current freq: %d', self.__dev.get_pwm_frequency())
        self.__logger.info('Requested freq: %d', freq)

        if(freq == self.__dev.get_pwm_frequency()):
            return

        self.__dev.set_pwm_frequency(freq)

    def turn_on(self):
        """
        Turn on the PWM provider at the set duty cycle
        """
        self.__dev.set_pwm(self.__pin, self.__duty)

    def turn_off(self):
        """
        Turn off the PWM provider
        """
        self.__dev.set_pwm(self.__pin, 0)

