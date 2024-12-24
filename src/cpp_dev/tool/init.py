# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from typing import Optional

from filelock import FileLock, Timeout


###############################################################################
# Public API                                                                ###
###############################################################################


def assert_cpd_is_initialized(base_dir: Path = Path.home()) -> None:
    """
    Check that cpd is properly initialized, e.g. that the Conan folder exists.
    """
    conan_dir = _compose_conan_home(_compose_cpd_dir(base_dir))
    if not conan_dir.exists():
        raise RuntimeError(
            "cpd is not yet properly initialized, please run 'cpd tool init' first"
        )


def initialize_cpd(base_dir: Path = Path.home()) -> None:
    """
    Initialize cpd to have all configurations properly setup.

    This operation uses a file lock to assure that the initialization is done
    without inteference from other executions.
    """
    cpd_dir = _compose_cpd_dir(base_dir)
    cpd_dir.mkdir(parents=True, exist_ok=True)
    init_lock = _compose_init_lock_file(cpd_dir)
    try:
        with init_lock:
            _initialize_cpd(cpd_dir)
    except Timeout:
        raise RuntimeError("The cpd init operation is already in progress.")


def get_cpd_dir(base_dir: Path = Path.home()) -> Path:
    """
    Return the path to the cpd tool directory.
    """
    return _compose_cpd_dir(base_dir)


def get_conan_home(base_dir: Path = Path.home()) -> Path:
    """
    Return the path to the Conan home directory.
    """
    return _compose_conan_home(_compose_cpd_dir(base_dir))


###############################################################################
# Implementation                                                            ###
###############################################################################


def _initialize_cpd(cpd_dir: Path) -> None:
    _initialize_conan(cpd_dir)


def _initialize_conan(cpd_dir: Path) -> None:
    pass


def _compose_init_lock_file(cpd_dir: Path, timeout: Optional[float] = None) -> FileLock:
    return FileLock(
        cpd_dir / ".init_lock", timeout=timeout if timeout is not None else -1
    )


def _compose_cpd_dir(base_dir: Path) -> Path:
    return base_dir / ".cpd"


def _compose_conan_home(cpd_dir: Path) -> Path:
    return cpd_dir / "conan2"
