class DecoraBLEError(Exception):
    """Base class for DecoraBLE related errors"""


class DeviceNotInPairingModeError(DecoraBLEError):
    """Raised when attempting to pair with a device that is not in pairing mode."""


class IncorrectAPIKeyError(DecoraBLEError):
    """Raised when a characteristic is missing."""


class DeviceConnectionError(DecoraBLEError):
    """ Raised in connecting to the device """


class DeviceConnectionTimeoutError(DecoraBLEError):
    """Timeout waiting for device connection."""
