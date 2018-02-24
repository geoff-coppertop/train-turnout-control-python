#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# test_pwm_provider_pca9685.py
#
# G. Thomas
# 2018
#-------------------------------------------------------------------------------

import logging
import pytest

from tests.hw.pwm.fake_pwm_provider import FakePWMProvider
from src.hw.gpio.gpo_provider_pwm import GPOProviderPWM

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture
def pwm_provider():
    """Creates a fake pwm provider for testing"""
    return FakePWMProvider()

@pytest.fixture
def gpo_provider(pwm_provider):
    """Creates a gpo provider for testing"""
    return GPOProviderPWM(pwm_provider)
#-------------------------------------------------------------------------------
# Init tests
#-------------------------------------------------------------------------------
def test_init_gpo(pwm_provider):
    """Test that normal creation leaves the output off"""
    GPOProviderPWM(pwm_provider)

    assert(pwm_provider.get_duty() == 100)
    assert(not pwm_provider.output_enabled())

def test_init_gpo_pwm_gt_0_on(pwm_provider):
    """Test that creation with an enabled output leaves the output off"""
    pwm_provider.set_duty(50)
    pwm_provider.turn_on()

    GPOProviderPWM(pwm_provider)

    assert(pwm_provider.get_duty() == 100)
    assert(not pwm_provider.output_enabled())

#-------------------------------------------------------------------------------
# Output tests
#-------------------------------------------------------------------------------
def test_output_on(gpo_provider, pwm_provider):
    assert(not pwm_provider.output_enabled())

    gpo_provider.enable()

    assert(pwm_provider.get_duty() == 100)
    assert(pwm_provider.output_enabled())

def test_output_on_off(gpo_provider, pwm_provider):

    gpo_provider.enable()
    gpo_provider.disable()

    assert(pwm_provider.get_on_count() == 1)
    assert(pwm_provider.get_duty() == 100)
    assert(not pwm_provider.output_enabled())

def test_output_on_on(gpo_provider, pwm_provider):

    gpo_provider.enable()
    gpo_provider.enable()

    assert(pwm_provider.get_on_count() == 2)
    assert(pwm_provider.output_enabled())

def test_output_on_off_on(gpo_provider, pwm_provider):

    gpo_provider.enable()
    gpo_provider.disable()
    gpo_provider.enable()

    assert(pwm_provider.get_on_count() == 2)
    assert(pwm_provider.output_enabled())
