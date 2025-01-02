# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from dataclasses import dataclass
from enum import Enum

import distro

###############################################################################
# Public API                                                                ###
###############################################################################


class OperatingSystemType(Enum):
    """Enumeration of supported operating system types."""

    Ubuntu2404 = "Ubuntu 24.04"
    Unsupported = "unsupported"


@dataclass
class OperatingSystem:
    """Data class representing an operating system."""

    type: OperatingSystemType
    name: str
    version: str


def assert_supported_os() -> None:
    """Assert that the current operating system is supported by cpd."""
    os = detect_os()
    if os.type == OperatingSystemType.Unsupported:
        msg = f"Unsupported operating system: {os.name} {os.version}"
        raise RuntimeError(msg)


def detect_os() -> OperatingSystem:
    """Detect the current operating system: id, name and version."""
    distro_id = distro.id()
    distro_name = distro.name(pretty=True)
    distro_version = distro.version(best=True)
    if distro_id == "ubuntu":
        return _detect_ubuntu(distro_name, distro_version)
    return _construct_unsupported_os(
        name=distro_name,
        version=distro_version,
    )


def get_supported_os() -> list[OperatingSystemType]:
    """Return a list of supported operating system types."""
    return [
        OperatingSystemType.Ubuntu2404,
    ]


###############################################################################
# Implementation                                                            ###
###############################################################################


def _detect_ubuntu(name: str, version: str) -> OperatingSystem:
    if version.startswith("24.04"):
        return OperatingSystem(
            type=OperatingSystemType.Ubuntu2404,
            name=name,
            version=version,
        )

    return _construct_unsupported_os(
        name=name,
        version=version,
    )


def _construct_unsupported_os(name: str, version: str) -> OperatingSystem:
    return OperatingSystem(
        type=OperatingSystemType.Unsupported,
        name=name,
        version=version,
    )
