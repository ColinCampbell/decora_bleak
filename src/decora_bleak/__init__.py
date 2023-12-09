#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Copyright (c) 2023 Colin Campbell
# MIT license
# This code was inspired by https://github.com/mjg59/python-decora and https://github.com/lucapinello/pydecora_ble/tree/master

__version__ = "0.2.2"

from .const import DECORA_SERVICE_UUID
from .decora_bleak import DecoraBLEDevice
from .exceptions import DeviceConnectionError, DeviceNotInPairingModeError, IncorrectAPIKeyError, DecoraBLEError, DeviceConnectionTimeoutError
from .models import DecoraBLEDeviceState, DecoraBLEDeviceSummary

__all__ = [
    "DECORA_SERVICE_UUID",
    "DecoraBLEDevice",
    "DecoraBLEDeviceState",
    "DecoraBLEDeviceSummary",
    "BLEAK_EXCEPTIONS",
    "DecoraBLEError",
    "DeviceConnectionError",
    "DeviceConnectionTimeoutError",
    "DeviceNotInPairingModeError",
    "IncorrectAPIKeyError"
]
