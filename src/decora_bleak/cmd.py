#!/usr/bin/env python3

import argparse
import asyncio
import json
import logging
import sys
from typing import Optional

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from . import DecoraBLEDevice, DECORA_SERVICE_UUID, DeviceConnectionError, DeviceNotInPairingModeError, IncorrectAPIKeyError

_LOGGER = logging.getLogger(__name__)

stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=handlers)

_LOGGER.setLevel(logging.FATAL)
logging.getLogger("decora_bleak").setLevel(logging.ERROR)


async def scan() -> None:
    print("Discovering devices...")
    devices = await BleakScanner.discover(timeout=10, service_uuids=[DECORA_SERVICE_UUID])

    if len(devices) > 0:
        print('\t\n'.join(
            [f"{device.name} - address: {device.address}" for device in devices]))
    else:
        print("Did not discover any Decora devices, try moving closer to the switch or trying again")


async def summarize(address: str, api_key: str) -> None:
    device = await _find_device(address)
    if device is None:
        _LOGGER.error("Could not find device at %s, please try again", address)
        return

    def connection_callback(summary):
        print(f"{summary}")

    decora_device = DecoraBLEDevice(device, api_key)
    unregister_connection_callback = decora_device.register_connection_callback(connection_callback)

    def state_callback(state):
        if state.is_on:
            print(
                f"Light is turned on ({state.brightness_level}% brightness)")
        else:
            print("Light is turned off")
    unregister_state_callback = decora_device.register_state_callback(state_callback)

    await decora_device.connect()

    unregister_connection_callback()
    unregister_state_callback()

    await decora_device.disconnect()


async def connect(address: str, api_key: Optional[str]) -> None:
    device = await _find_device(address)
    if device is None:
        _LOGGER.error("Could not find device at %s, please try again", address)
        return

    if api_key is None:
        try:
            api_key = await DecoraBLEDevice.get_api_key(device)
        except DeviceNotInPairingModeError as ex:
            _LOGGER.error(ex)
            print(f"Device not in pairing mode, hold down on the switch for a few seconds until a green light flashes")
            return
        except DeviceConnectionError as ex:
            _LOGGER.error(ex)
            print(f"Connection error: {ex}")
            return
        except Exception as ex:
            _LOGGER.error(ex)
            print(f"Unexpected error occurred")
            return

        print(f"Fetched API key from device: {api_key}")

    if api_key is not None:
        print(f"Connecting to device at {device.address} with key: {api_key}")

        decora_device = DecoraBLEDevice(device, api_key)
        try:
            await decora_device.connect()
        except IncorrectAPIKeyError as ex:
            _LOGGER.error(ex)
            print("Incorrect API key, try putting the device into pairing mode and reinvoking the script without an API key argument")
            return
        except DeviceConnectionError as ex:
            _LOGGER.error(ex)
            print(f"Connection error: {ex}")
            return
        except Exception as ex:
            _LOGGER.error(ex)
            print(f"Unexpected error: {ex}")
            return

        def state_callback(state):
            if state.is_on:
                print(
                    f"Light is now turned on ({state.brightness_level}% brightness)")
            else:
                print("Light is now turned off")
        unregister_callback = decora_device.register_state_callback(state_callback)

        await decora_device.turn_on(brightness_level=100)
        await asyncio.sleep(5)
        await decora_device.turn_off()
        await asyncio.sleep(5)
        await decora_device.turn_on()
        await asyncio.sleep(5)
        await decora_device.set_brightness_level(50)

        unregister_callback()
        await decora_device.disconnect()
    else:
        _LOGGER.error(
            "Switch is not in pairing mode - hold down until green light flashes and execute this function again")


async def _find_device(address: str) -> Optional[BLEDevice]:
    future: asyncio.Future[BLEDevice] = asyncio.Future()

    def on_detected(device: BLEDevice, adv: AdvertisementData) -> None:
        if future.done():
            return

        if device.address.lower() == address.lower():
            _LOGGER.info("Found device: %s", device.address)
            future.set_result(device)

    scanner = BleakScanner(detection_callback=on_detected)
    await scanner.start()

    device = await future
    await scanner.stop()

    return device


def main():
    parser = argparse.ArgumentParser(
        description="Interact with Decora BLE devices")
    subparsers = parser.add_subparsers(dest="subparser")

    scan_subparser = subparsers.add_parser("scan")

    summarize_subparser = subparsers.add_parser("summarize")
    summarize_subparser.add_argument("-a", "--address", dest="address")
    summarize_subparser.add_argument(
        "-k", "--api-key", dest="api_key")

    connect_subparser = subparsers.add_parser("connect")
    connect_subparser.add_argument("-a", "--address", dest="address")
    connect_subparser.add_argument(
        "-k", "--api-key", dest="api_key", nargs="?")

    kwargs = vars(parser.parse_args())
    asyncio.run(globals()[kwargs.pop('subparser')](**kwargs))
