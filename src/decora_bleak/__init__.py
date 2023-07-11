#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# Copyright (c) 2023 Colin Campbell
# MIT license
# This code was inspired by https://github.com/mjg59/python-decora and https://github.com/lucapinello/pydecora_ble/tree/master

__version__ = "0.0.0"

from .decora_bleak import DecoraBLEDevice
from .const import DECORA_SERVICE_UUID

__all__ = [
    "DECORA_SERVICE_UUID",
    "DecoraBLEDevice",
]
