# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from cpp_dev.common.process import run_command
from cpp_dev.common.utils import updated_env
from cpp_dev.conan.config import get_conan_config_source_dir, get_remotes

###############################################################################
# Public API                                                                ###
###############################################################################


CONAN_HOME_ENV_VAR = "CONAN_HOME"


def initialize_conan(conan_home: Path) -> None:
    """Initialize Conan to use the given home directory."""
    with _conan_env(conan_home):
        conan_config_dir = get_conan_config_source_dir()
        _install_conan_config(conan_config_dir)
        _set_conan_default_user_and_password(conan_config_dir)


###############################################################################
# Implementation                                                            ###
###############################################################################

# The default Conan user and password are used to authenticate against the Conan
# Important: this user has only READ permissions which is required to download packages
# and obtain meta data.
_DEFAULT_CONAN_USER = "cpd_default"
_DEFAULT_CONAN_USER_PWD = "Cpd-Dev.1"  # noqa: S105


@contextmanager
def _conan_env(conan_home: Path) -> Generator[None]:
    with updated_env(**{CONAN_HOME_ENV_VAR: str(conan_home)}):
        yield


def _install_conan_config(conan_config_dir: Path) -> None:
    run_command("conan", "config", "install", str(conan_config_dir))


def _set_conan_default_user_and_password(conan_config_dir: Path) -> None:
    conan_remotes = get_remotes(conan_config_dir)
    for remote in conan_remotes.remotes:
        run_command(
            "conan",
            "remote",
            "login",
            remote.name,
            _DEFAULT_CONAN_USER,
            "-p",
            _DEFAULT_CONAN_USER_PWD,
        )
