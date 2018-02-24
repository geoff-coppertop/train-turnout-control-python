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

from fake_pca9685 import FakePCA9685
from src.hw.pwm.pwm_provider_pca9685 import PWMProviderPCA9685

#-------------------------------------------------------------------------------
# Test fixtures
#-------------------------------------------------------------------------------
@pytest.fixture()
def device():
    """Creates a fake PCA9685 to be used during the test"""
    return FakePCA9685()

@pytest.fixture
def pwm_provider(device):
    """Creates a PCA9685 pwm provider for testing"""
    return PWMProviderPCA9685(device, 0)

#-------------------------------------------------------------------------------
# Init tests
#-------------------------------------------------------------------------------
def test_init_pwm(device):
    """Test that normal creation sets freq and duty to 0"""
    PWMProviderPCA9685(device, 0)
    assert(device.get_pwm()==0)
    assert(device.get_pwm_frequency()==0)

# TODO: These next two tests can probably be parameterized
def test_init_pwm_invalid_pin_low(device):
    """Test pwm provider creation with an invalid low pin"""
    with pytest.raises(AssertionError):
        PWMProviderPCA9685(device, -20)

def test_init_pwm_invalid_pin_high(device):
    """Test pwm provider creation with an invalid high pin"""
    with pytest.raises(AssertionError):
        PWMProviderPCA9685(device, 20)

#-------------------------------------------------------------------------------
# Duty cycle tests
#-------------------------------------------------------------------------------
def test_set_duty_in_range_off(pwm_provider, device):
    """Check that the device doesn't output until turned on"""
    pwm_provider.set_duty(50)
    assert(device.get_pwm()==0)

def test_set_duty_in_range_on(pwm_provider, device):
    """Chaeck that the device outputs when turned on"""
    pwm_provider.set_duty(50)
    pwm_provider.turn_on()
    assert(device.get_pwm()==int(0.5 * 0x0FFF))

def test_set_duty_in_range_on_off(pwm_provider, device):
    """Check that the device doesn't output when turned off"""
    pwm_provider.set_duty(50)
    pwm_provider.turn_on()
    pwm_provider.turn_off()
    assert(device.get_pwm()==0)

def test_set_duty_in_range_on_off_on(pwm_provider, device):
    """Check that the device outputs at the desired duty cycle when
    re-enabled
    """
    pwm_provider.set_duty(50)
    pwm_provider.turn_on()
    pwm_provider.turn_off()
    pwm_provider.turn_on()
    assert(device.get_pwm()==int(0.5 * 0x0FFF))

# TODO: These next two tests can probably be parameterized
def test_set_duty_out_range_low(pwm_provider, device):
    """Check that device asserts when duty cycle out of range low"""
    with pytest.raises(AssertionError):
        pwm_provider.set_duty(-10)

def test_set_duty_out_range_high(pwm_provider, device):
    """Check that device asserts when duty cycle out of range high"""
    with pytest.raises(AssertionError):
        pwm_provider.set_duty(110)

#-------------------------------------------------------------------------------
# Frequency tests
#-------------------------------------------------------------------------------
def test_set_freq_in_range(pwm_provider, device):
    """Set the device to a valid frequency"""
    pwm_provider.set_freq(50)
    assert(device.get_pwm_frequency()==50)

def test_set_same_freq_in_range(pwm_provider, device):
    """Set the device to a valid frequency"""
    pwm_provider.set_freq(50)
    pwm_provider.set_freq(50)
    assert(device.get_pwm_frequency()==50)

# TODO: These next two tests can probably be parameterized
def test_set_freq_out_range_low(pwm_provider, device):
    """Set the device to an invalid low frequency"""
    with pytest.raises(AssertionError):
        pwm_provider.set_freq(0)

def test_set_freq_out_range_high(pwm_provider, device):
    """Set the device to an invalid high frequency"""
    with pytest.raises(AssertionError):
        pwm_provider.set_freq(10000)
