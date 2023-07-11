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

from decora_bleak import DecoraBLEDevice, DECORA_SERVICE_UUID

_LOGGER = logging.getLogger(__name__)

stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler]

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=handlers)

_LOGGER.setLevel(logging.ERROR)
logging.getLogger("decora_bleak").setLevel(logging.ERROR)


async def scan() -> None:
    print("Discovering devices...")
    devices = await BleakScanner.discover(timeout=10, service_uuids=[DECORA_SERVICE_UUID])

    if len(devices) > 0:
        print('\t\n'.join([f"{device.name} - address: {device.address}" for device in devices]))
    else:
        print("Did not discover any Decora devices, try moving closer to the switch or trying again")


async def run(address: str, api_key: Optional[str]) -> None:
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

    if api_key is None:
        api_key = await DecoraBLEDevice.get_api_key(device)
        print(f"Fetched API key from device: {api_key}")

    if api_key is not None:
        _LOGGER.info("Connecting to device at %s with key: %s", device.address, api_key)

        decora_device = DecoraBLEDevice()
        await decora_device.connect(device, api_key)
        await decora_device.turn_on()
        await asyncio.sleep(5)
        await decora_device.turn_off()
        await asyncio.sleep(5)
        await decora_device.turn_on()
        await asyncio.sleep(5)
        await decora_device.set_brightness_level(50)

        await decora_device.disconnect()
    else:
        _LOGGER.error("Switch is not in pairing mode - hold down until green light flashes and execute this function again")


parser = argparse.ArgumentParser(description="Interact with a Decora BLE device")
parser.add_argument("--address", nargs="?")
parser.add_argument("--api-key", nargs="?")

async def main():
    args = parser.parse_args()
    _LOGGER.debug("%s", args)

    address = args.address
    if address is not None:
        await run(address, args.api_key)
    else:
        await scan()

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = None

if loop and loop.is_running():
    task = loop.create_task(main())
    task.add_done_callback(
        lambda t: _LOGGER.debug(f'main finished with result:{t.result}')
    )
else:
    result = asyncio.run(main())
