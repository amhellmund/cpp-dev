# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from pydantic import BaseModel

from cpp_dev.common.types import SemanticVersion

###############################################################################
# Public API                                                                ###
###############################################################################


def get_cpd_version_from_code() -> SemanticVersion:
    """Get the version of the cpd tool."""
    return SemanticVersion.from_parts(
        major=_CPD_MAJOR_VERSION,
        minor=_CPD_MINOR_VERSION,
        patch=_CPD_PATCH_VERSION,
    )


def read_version_file(cpd_dir: Path) -> SemanticVersion:
    """Read the version file from the cpd directory."""
    version_file = cpd_dir / "version.txt"
    if not version_file.exists():
        raise RuntimeError(f"The version file {version_file} does not exist.")
    with version_file.open() as f:
        return SemanticVersion(f.read().strip())


def write_version_file(cpd_dir: Path, version: SemanticVersion) -> None:
    """Write the version file to the cpd directory."""
    version_file = cpd_dir / "version.txt"
    with version_file.open("w") as f:
        f.write(str(version))


###############################################################################
# Implementation                                                            ###
###############################################################################

_CPD_MAJOR_VERSION = 0
_CPD_MINOR_VERSION = 0
_CPD_PATCH_VERSION = 0
