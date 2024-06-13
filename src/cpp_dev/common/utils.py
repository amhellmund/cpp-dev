# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from pathlib import Path
import re


def is_valid_name(name: str) -> bool:
    return re.match(r"^[a-z][a-z_]*$", name) is not None


def ensure_dir_exists(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
