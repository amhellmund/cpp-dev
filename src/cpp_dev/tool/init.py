# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from filelock import FileLock, Timeout

from cpp_dev.common.utils import ensure_dir_exists
from cpp_dev.conan.commands import initialize_conan
from cpp_dev.tool.version import get_cpd_version_from_code, write_version_file

###############################################################################
# Public API                                                                ###
###############################################################################


def assure_cpd_is_initialized(base_dir: Path | None = None) -> None:
    """Check that cpd is properly initialized, e.g. that the Conan folder exists."""
    cpd_dir = _compose_cpd_dir(_get_base_dir_or_home(base_dir))
    conan_dir = _compose_conan_home(cpd_dir)
    if not conan_dir.exists():
        initialize_cpd(cpd_dir)
    else:
        update_cpd(cpd_dir)


def initialize_cpd(base_dir: Path | None = None) -> None:
    """Initialize cpd to have all configurations properly setup.

    This operation uses a file lock to assure that the initialization is done
    without inteference from other executions.
    """
    cpd_dir = _compose_cpd_dir(_get_base_dir_or_home(base_dir))
    ensure_dir_exists(cpd_dir)
    init_lock = _compose_init_lock_file(cpd_dir)
    try:
        with init_lock:
            _initialize_cpd(cpd_dir)
    except Timeout as e:
        raise RuntimeError("The cpd init operation is already in progress.") from e


# def update_cpd(base_dir: Path | None = None) -> None:
#     """Update cpd to have all configurations properly setup."""
#     cpd_dir = _compose_cpd_dir(_get_base_dir_or_home(base_dir))
#     cpd_tool_version_in_code = get_cpd_version_from_code()
#     cpd_version_installed = read_version_file(cpd_dir)
#     if (cpd)


def get_cpd_dir(base_dir: Path | None = None) -> Path:
    """Return the path to the cpd directory."""
    return _compose_cpd_dir(_get_base_dir_or_home(base_dir))


def get_conan_home(base_dir: Path | None = None) -> Path:
    """Return the path to the Conan home directory."""
    return _compose_conan_home(_compose_cpd_dir(_get_base_dir_or_home(base_dir)))


###############################################################################
# Implementation                                                            ###
###############################################################################


def _get_base_dir_or_home(base_dir: Path | None = None) -> Path:
    return base_dir if base_dir is not None else Path.home()


def _initialize_cpd(cpd_dir: Path) -> None:
    _initialize_conan(cpd_dir)


def _initialize_conan(cpd_dir: Path) -> None:
    conan_dir = _compose_conan_home(cpd_dir)
    ensure_dir_exists(conan_dir)
    initialize_conan(conan_dir)
    write_version_file(cpd_dir, get_cpd_version_from_code())


def _compose_init_lock_file(cpd_dir: Path, timeout: float | None = None) -> FileLock:
    return FileLock(cpd_dir / ".init_lock", timeout=timeout if timeout is not None else -1)


def _compose_cpd_dir(base_dir: Path) -> Path:
    return base_dir / ".cpd"


def _compose_conan_home(cpd_dir: Path) -> Path:
    return cpd_dir / "conan2"
