# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from cpp_dev.common.utils import updated_env
from cpp_dev.common.process import run_command

###############################################################################
# Public API                                                                ###
###############################################################################


CONAN_HOME_ENV_VAR = "CONAN_HOME"


def initialize_conan(conan_home: Path) -> None:
    """
    Initializes Conan to use the given home directory.
    """
    with _conan_env(conan_home):
        conan_config_dir = _compose_conan_config_source_dir()
        _install_conan_config(conan_config_dir)


###############################################################################
# Implementation                                                            ###
###############################################################################


@contextmanager
def _conan_env(conan_home: Path) -> Generator[None, None, None]:
    with updated_env(**{CONAN_HOME_ENV_VAR: str(conan_home)}):
        yield


def _install_conan_config(conan_config_source_dir: Path) -> None:
    result = run_command("conan", "config", "install", str(conan_config_source_dir))
    if result.returncode != 0:
        raise RuntimeError("Failed to install Conan configuration.")


def _compose_conan_config_source_dir() -> Path:
    this_script_dir = Path(__file__).parent
    return this_script_dir.parent.parent.parent / "conan"
