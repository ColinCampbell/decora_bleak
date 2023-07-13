from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import Optional
from dataclasses import replace

from bleak import BleakClient, BleakGATTCharacteristic
from bleak.backends.device import BLEDevice

from .const import EVENT_CHARACTERISTIC_UUID, STATE_CHARACTERISTIC_UUID, UNPAIRED_API_KEY
from .models import DecoraBLEDeviceState

_LOGGER = logging.getLogger(__name__)



class DecoraBLEDevice():
    def __init__(self):
        self._client = None
        self._device = None
        self._key = None
        self._state = DecoraBLEDeviceState()
        self._state_callbacks: list[Callable[[DecoraBLEDeviceState], None]] = []

    async def get_api_key(device: BLEDevice) -> Optional[str]:
        async with BleakClient(device) as client:
            await client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, bytearray([0x22, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]), response=True)
            rawkey = await client.read_gatt_char(EVENT_CHARACTERISTIC_UUID)
            _LOGGER.debug("Raw API key from device: %s", repr(rawkey))

            if rawkey[2:6] != UNPAIRED_API_KEY:
                return bytearray(rawkey)[2:].hex()
            else:
                return None

    async def register_state_callback(
        self, callback: Callable[[DecoraBLEDeviceState], None]
    ) -> Callable[[], None]:
        def unregister_callback() ->  None:
            self._state_callbacks.remove(callback)

        self._state_callbacks.append(callback)
        return unregister_callback

    async def connect(self, device: BLEDevice, key: str) -> None:
        _LOGGER.debug("attempting to connect to %s using %s key", device.address, key)

        if self._client is not None and self._client.is_connected:
            _LOGGER.debug("there is already a client connected, disconnecting...")
            self._client.disconnect()

        self._device = device
        self._key = bytearray.fromhex(key)

        def disconnected(client):
            _LOGGER.debug("Device disconnected %s", device.address)
            self._disconnect_cleanup()

        self._client = BleakClient(device, disconnected_callback=disconnected)

        await self._client.connect()
        await self._unlock()

        await self._register_for_state_notifications()

        _LOGGER.debug("Finished connecting %s", self._client.is_connected)

    async def disconnect(self) -> None:
        await self._client.disconnect()

    async def turn_on(self) -> None:
        _LOGGER.debug("Turning on...")
        await self._write_state(replace(self._state, is_on=True))

    async def turn_off(self) -> None:
        _LOGGER.debug("Turning off...")
        await self._write_state(replace(self._state, is_on=False))

    async def set_brightness_level(self, brightness_level: int):
        _LOGGER.debug("Setting brightness level to %d...", brightness_level)
        await self._write_state(replace(self._state, brightness_level=brightness_level))

    def _disconnect_cleanup(self):
        self._device = None
        self._key = None
        self._client = None
        self._state = DecoraBLEDeviceState()

    async def _unlock(self):
        packet = bytearray([0x11, 0x53, *self._key])
        await self._client.write_gatt_char(EVENT_CHARACTERISTIC_UUID, packet, response=True)

    def _apply_device_state_data(self, data: bytearray) -> None:
        self._state = replace(self._state, is_on=data[0] == 1, brightness_level=data[1])
        _LOGGER.debug("State updated: %s", self._state)

    async def _write_state(self, state: DecoraBLEDeviceState) -> None:
        self._state = state
        packet = bytearray([1 if state.is_on else 0, state.brightness_level])
        _LOGGER.debug("Writing state: %s", state)
        await self._client.write_gatt_char(STATE_CHARACTERISTIC_UUID, packet, response=True)

    async def _register_for_state_notifications(self) -> None:
        def callback(sender: BleakGATTCharacteristic, data: bytearray) -> None:
            self._apply_device_state_data(data)
            self._fire_state_callbacks()

        self._client.start_notify(STATE_CHARACTERISTIC_UUID, callback)

    def _fire_state_callbacks(self) -> None:
        for callback in self._state_callbacks:
            callback(self._state)
