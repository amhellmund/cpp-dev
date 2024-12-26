# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from pydantic import BaseModel

###############################################################################
# Public API                                                                ###
###############################################################################


def get_conan_config_source_dir() -> Path:
    """Get the directory containing the Conan configuration files in the source tree.

    Important: the configuration gets installed into the CONAN_HOME directory during the
    tool setup. The directory returned by this function is used to install the configuration
    files.
    """
    return Path(__file__).parent / "config"


class ConanRemote(BaseModel):
    """A Conan remote."""

    name: str
    url: str
    verify_ssl: bool


class ConanRemotes(BaseModel):
    """A list of Conan remotes."""

    remotes: list[ConanRemote]


def get_remotes(conan_config_dir: Path) -> ConanRemotes:
    """Get the Conan remotes from the given configuration directory."""
    remotes_file = conan_config_dir / "remotes.json"
    return ConanRemotes.model_validate_json(remotes_file.read_text())
