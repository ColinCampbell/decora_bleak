#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Copyright (c) 2023 Colin Campbell
# MIT license
# This code was inspired by https://github.com/mjg59/python-decora and https://github.com/lucapinello/pydecora_ble/tree/master

__version__ = "0.1.0"

from .const import DECORA_SERVICE_UUID
from .decora_bleak import BLEAK_EXCEPTIONS, DecoraBLEDevice
from .exceptions import DeviceNotInPairingModeError, IncorrectAPIKeyError
from .models import DecoraBLEDeviceState, DecoraBLEDeviceSummary

__all__ = [
    "DECORA_SERVICE_UUID",
    "DecoraBLEDevice",
    "DecoraBLEDeviceState",
    "DecoraBLEDeviceSummary",
    "BLEAK_EXCEPTIONS",
    "DeviceNotInPairingModeError",
    "IncorrectAPIKeyError"
]
