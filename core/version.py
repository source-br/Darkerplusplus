"""Centralized version information for Hammerfy."""

__version__ = "0.1.0-beta"

# Developer Mode flag — set to False before building production releases
DEV_MODE = True


def get_version() -> str:
    """Returns the current application version string."""
    return __version__


def is_dev_mode() -> bool:
    """Returns True if developer mode features should be enabled in the UI."""
    return DEV_MODE
