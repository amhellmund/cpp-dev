# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from .command_wrapper import conan_config_install, conan_remote_login
from .utils import conan_env

###############################################################################
# Public API                                                                ###
###############################################################################

CONAN_REMOTE = "cpd"

# The default Conan user and password are used to authenticate against the Conan
# Important: this user has only READ permissions which is required to download packages
# and obtain meta data.
DEFAULT_CONAN_USER = "cpd_default"
DEFAULT_CONAN_USER_PWD = "Cpd-Dev.1"  # noqa: S105

def get_conan_config_source_dir() -> Path:
    """Get the directory containing the Conan configuration files in the source tree.

    Important: the configuration gets installed into the CONAN_HOME directory during the
    tool setup. The directory returned by this function is used to install the configuration
    files.
    """
    return Path(__file__).parent / "config"



def initialize_conan(conan_home: Path) -> None:
    """Initialize Conan to use the given home directory."""
    with conan_env(conan_home):
        conan_config_dir = get_conan_config_source_dir()
        conan_config_install(conan_config_dir)
        conan_remote_login(CONAN_REMOTE, DEFAULT_CONAN_USER, DEFAULT_CONAN_USER_PWD)
