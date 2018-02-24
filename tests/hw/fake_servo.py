#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# fake_servo.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

class FakeServo(object):
    """Servo test double implementation"""

    def __init__(self):
        """Create a servo test double, angle initialized to 90 degrees"""
        self.__logger = logging.getLogger('fake_servo')

        self.__angle = 90

    def set_angle(self, angle):
        """Move servo to desired angle"""
        assert(angle >= 0)
        assert(angle <= 180)

        self.__angle = angle

    def get_angle(self):
        """Return current servo angle"""
        return self.__angle



