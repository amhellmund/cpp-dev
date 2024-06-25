# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from contextlib import contextmanager
from pathlib import Path
import re
from typing import Generator, Optional
from tempfile import TemporaryDirectory


def is_valid_name(name: str) -> bool:
    """
    Check if a string is a valid cpp-dev name identifier.

    A valid cpp-dev name identifier must start with a lowercase letter and
    only contain lowercase letters and underscores.
    """
    return re.match(r"^[a-z][a-z_]*$", name) is not None


def ensure_dir_exists(path: Path) -> Path:
    """
    Ensure that a directory exists.

    Returns the path to the directory for caller convenience.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def create_tmp_dir(base: Optional[Path] = None) -> Generator[Path, None, None]:
    """
    Creates a temporary directory and yields its path.

    The base directory can be specified. If not provided, the system's default temporary directory is used.
    """
    with TemporaryDirectory(dir=base) as tmp_dir:
        yield Path(tmp_dir)
