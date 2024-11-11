# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from cpp_dev.common.utils import ensure_dir_exists
from cpp_dev.package.types import PackageFileSpecs
from cpp_dev.packaging.core import create_package


def _create_file_with_content(file_path: Path) -> Path:
    ensure_dir_exists(file_path.parent)
    file_path.touch()
    file_path.write_text(file_path.name)
    return file_path


def _create_simple_package(target_dir: Path) -> PackageFileSpecs:
    ensure_dir_exists(target_dir)

    binaries = [_create_file_with_content(target_dir / "bin" / "binary")]
    libraries = [_create_file_with_content(target_dir / "lib" / "library")]
    include_dir = target_dir / "include" / "package"
    _create_file_with_content(include_dir / "header")

    return PackageFileSpecs(
        binaries=binaries, libraries=libraries, includes=[include_dir]
    )


def test_create_package(tmp_path):
    specs = _create_simple_package(tmp_path / "source")

    create_package(specs, tmp_path / "package.zip")
