#!/usr/bin/env python
# # -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test_servo.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import pytest

from tests.hw.pwm.fake_pwm_provider import FakePWMProvider
from src.hw.servo import Servo

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture
def pwm_provider():
    """Creates a fake pwm provider for testing"""
    return FakePWMProvider()

@pytest.fixture
def servo(pwm_provider):
    """Creates a servo for testing"""
    return Servo(pwm_provider)

#-------------------------------------------------------------------------------
# Angle tests
#-------------------------------------------------------------------------------
@pytest.mark.parametrize("angle", [
    pytest.param(-10, marks=pytest.mark.xfail),
    0,
    45,
    90,
    135,
    180,
    pytest.param(190, marks=pytest.mark.xfail)])
def test_servo_angle(servo, pwm_provider, angle):
    """Check that requested angle generates a suitable duty cycle"""
    # Set angle will assert an error if an invalid angle is requested
    servo.set_angle(angle)

    # Check that the duty cycle is within limits 5%(1.0ms) to 10%(2.0ms)
    assert(pwm_provider.get_duty() >= 5)
    assert(pwm_provider.get_duty() <= 10)

def test_servo_repeat_angle(servo, pwm_provider):
    """Check that repeated requests for the same angle caus the output to be turned on"""

    # Set angle will assert an error if an invalid angle is requested
    servo.set_angle(90)

    # Check that the output was turned on
    assert(pwm_provider.get_on_count() == 1)

    # Set an in range angle
    servo.set_angle(90)

    # Check that the output was turned on again
    assert(pwm_provider.get_on_count() == 2)

def test_servo_signal_generation(servo, pwm_provider):
    """Check that the PWM signal goes off-on-off on angle request"""

    # Check that output starts turned off
    assert(not pwm_provider.output_enabled())

    # Check that the output has not been turned on
    assert(pwm_provider.get_on_count() == 0)

    # Set angle will assert an error if an invalid angle is requested
    servo.set_angle(90)

    # Check that output is again off
    assert(not pwm_provider.output_enabled())

    # Check that the output has been turned on
    assert(pwm_provider.get_on_count() == 1)



#-------------------------------------------------------------------------------
# Frequency tests
#-------------------------------------------------------------------------------
def test_servo_freq(servo, pwm_provider):
    # Set the frequency to something invalid for a servo
    pwm_provider.set_freq(1000)

    # Set the servo angle to something, servo is assumed to be off beforehand
    servo.set_angle(90)

    # Check that the expected frequency has been requested
    assert(pwm_provider.get_freq() == 50)
