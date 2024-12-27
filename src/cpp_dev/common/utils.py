# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import os
import re
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory


def is_valid_name(name: str) -> bool:
    """Check if a string is a valid cpp-dev name identifier.

    A valid cpp-dev name identifier must start with a lowercase letter and
    only contain lowercase letters and underscores.
    """
    return re.match(r"^[a-z][a-z_]*$", name) is not None


def ensure_dir_exists(path: Path) -> Path:
    """Ensure that a directory exists.

    Returns the path to the directory for caller convenience.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def create_tmp_dir(base: Path | None = None) -> Generator[Path]:
    """Create a temporary directory and yields its path.

    The base directory can be specified. If not provided, the system's default temporary directory is used.
    """
    with TemporaryDirectory(dir=base) as tmp_dir:
        yield Path(tmp_dir)


@contextmanager
def updated_env(
    **new_or_modified_environ: object,
) -> Generator[None]:
    """Update the current system environment with the specified key/value pairs.

    This function supports the addition of new variables and modification of existing variables.
    It does not support the removal of variables.
    """
    old_environ = dict(os.environ)
    os.environ.update({key: str(value) for key, value in new_or_modified_environ.items()})
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
