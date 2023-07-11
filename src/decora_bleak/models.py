from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecoraBLEDeviceState:

    is_on: bool = False
    brightness_level: int = 0
