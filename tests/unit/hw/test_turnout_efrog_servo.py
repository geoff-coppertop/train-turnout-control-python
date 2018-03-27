#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test_turnout.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import pytest

from src.hw.turnout_efrog_servo import TurnoutEFrogServo

from tests.unit.hw.fake_servo import FakeServo
from tests.unit.hw.fake_gpo_provider import FakeGPOProvider

#-------------------------------------------------------------------------------
# Test constants
#-------------------------------------------------------------------------------
ANGLE_MAIN = 45
ANGLE_DIV = 135

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture
def servo():
    """Servo test double"""
    return FakeServo()

@pytest.fixture
def gpo_provider():
    """GPO provider test double"""
    return FakeGPOProvider()

@pytest.fixture
def turnout_main(servo, gpo_provider):
    """Create a turnout set to the diverging route"""
    turnout = TurnoutEFrogServo(servo, gpo_provider, ANGLE_MAIN, ANGLE_DIV)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_MAIN)
    assert(not gpo_provider.is_enabled())

    return turnout

@pytest.fixture
def turnout_div(turnout_main, servo, gpo_provider):
    """Create a turnout set to the diverging route"""
    turnout_main.set_route(True)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_DIV)
    assert(gpo_provider.is_enabled())

    return turnout_main

#-------------------------------------------------------------------------------
# Init tests
#-------------------------------------------------------------------------------
def test_init_bad_angle(servo, gpo_provider):
    """Chech that turnout init fails on bad limit angle"""
    with pytest.raises(AssertionError):
        TurnoutEFrogServo(servo, gpo_provider, -45, ANGLE_DIV)

#-------------------------------------------------------------------------------
# Route tests
#-------------------------------------------------------------------------------
def test_main_route(turnout_div, servo, gpo_provider):
    """Test that the turnout moves to the main route"""
    turnout_div.set_route(False)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_MAIN)
    assert(not gpo_provider.is_enabled())

def test_diverging_route(turnout_main, servo, gpo_provider):
    """Test that the turnout moves to the diverging route"""
    turnout_main.set_route(True)

    # Check that the route was set to the diverging route
    assert(servo.get_angle() == ANGLE_DIV)
    assert(gpo_provider.is_enabled())