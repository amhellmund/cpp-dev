# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from pathlib import Path

from cpp_dev.common.types import CppStandard

def setup_package (name: str, std: CppStandard, parent_dir: Path = Path.cwd()) -> Path:
    """
    Creates a new cpp-dev package in the specified parent directory.
    """