from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DecoraBLEDeviceState:

    is_on: bool = False
    brightness_level: int = 0


@dataclass(frozen=True)
class DecoraBLEDeviceSummary:

    system_identifier: str
    manufacturer: str
    model: str
    software_revision: Optional[str]
