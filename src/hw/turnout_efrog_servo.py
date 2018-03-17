#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# turnout.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging

class TurnoutEFrogServo(object):
    """Object for controlling an electro frog Turnout"""

    def __init__(self, servo, gpo_provider, main_angle, diverging_angle):
        """Create a turnout object

        Takes a servo to move the points along with the angles for the main and
        diverging angles, and a GPO to control the frog
        """
        self.__logger = logging.getLogger('turnout')

        self.__main_angle = main_angle
        self.__diverging_angle = diverging_angle
        self.__gpo = gpo_provider
        self.__servo = servo

        # Check that the given angles are within range
        assert(main_angle <= 180)
        assert(main_angle >= 0)

        assert(diverging_angle <= 180)
        assert(diverging_angle >= 0)

        # Align the turnout to the main route
        self.set_route(False)

    def set_route(self, diverging):
        """Set the route of the turnout"""

        angle = self.__main_angle
        text = 'Route set to main'

        if(diverging):
            angle = self.__diverging_angle
            text = 'Route set to diverging'
            self.__gpo.enable()
        else:
            self.__gpo.disable()

        self.__servo.set_angle(angle)
        self.__logger.info(text)

