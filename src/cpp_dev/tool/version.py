# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

###############################################################################
# Public API                                                                ###
###############################################################################


def get_cpd_version_from_code() -> str:
    """Get the version of the cpd tool."""
    return f"{_CPD_MAJOR_VERSION}.{_CPD_MINOR_VERSION}.{_CPD_PATCH_VERSION}"


def read_version_file(cpd_dir: Path) -> str:
    """Read the version file from the cpd directory."""
    version_file = cpd_dir / "version.txt"
    if not version_file.exists():
        raise RuntimeError(f"The version file {version_file} does not exist.")
    with version_file.open() as f:
        return f.read().strip()


def write_version_file(cpd_dir: Path) -> None:
    """Write the version file to the cpd directory."""
    version_file = cpd_dir / "version.txt"
    with version_file.open("w") as f:
        f.write(get_cpd_version_from_code())


###############################################################################
# Implementation                                                            ###
###############################################################################

_CPD_MAJOR_VERSION = 0
_CPD_MINOR_VERSION = 0
_CPD_PATCH_VERSION = 0
