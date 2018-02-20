#!/usr/bin/env python
# # -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# servo.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import time

from pwm import pwm_provider

class Servo(object):
    """Servo object that is able to go to a given angle using a PWM source"""

    def __init__(self, pwm_provider):
        """Create a servo object with a PWM source"""
        self.__logger = logging.getLogger('servo')

        self.__pwm = pwm_provider
        self.__angle = -90

    def set_angle(self, angle):
        """Sets the angle of the servo

        Makes sure the servo is only moved between min and max angle values.
        Gives 0.5s for the servo to move then the servo is turned off to reduce
        power consumption and keep things quiet.
        """

        # Check that the angle is in range
        assert(angle >= 0)
        assert(angle <= 180)

        # Do nothing if there is no change in angle from the last request
        if(self.__angle == angle):
            # Cause the servo to move to the previously set position
            self.__move()
            return
        else:
            self.__angle = angle

        # Calculate the duty cycle as a percentage
        # 50Hz => 20ms
        # 1ms => 0deg => 5%
        # 2ms => 180deg => 10%
        # duty = angle/180deg * (1ms * 50Hz / 1000) + (1ms * 50Hz / 1000)
        # duty = (1ms * 50Hz / 1000) * (1 + angle/180deg)
        duty = 5 * (1 + (angle / 180))

        # Set the desired position
        self.__pwm.set_duty(duty)

        # Cause the servo to move
        self.__move()

    def __move(self):
        """Move the servo to the set position"""

        # Make sure that the freq is set correctly
        self.__pwm.set_freq(50)

        self.__pwm.turn_on()

        # Allow time for transistion
        time.sleep(0.5)

        # Turn the servo off to reduce current and noise
        self.__pwm.turn_off()

