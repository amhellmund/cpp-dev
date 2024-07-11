# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import zipfile

from collections import Counter
from pathlib import Path
from cpp_dev.common.utils import create_tmp_dir, ensure_dir_exists
from cpp_dev.package.types import PackageFileSpecs
from shutil import copy, copytree


def create_package(file_specs: PackageFileSpecs, target_path: Path) -> None:
    _validate_file_specs(file_specs)

    with create_tmp_dir() as tmp_dir:
        _copy_file_paths_to_target(file_specs.binaries, tmp_dir / "bin")
        _copy_file_paths_to_target(file_specs.libraries, tmp_dir / "lib")
        _copy_dir_paths_to_target(file_specs.includes, tmp_dir / "include")
        _create_zip_archive(tmp_dir, target_path)


def _validate_file_specs(file_specs: PackageFileSpecs) -> None:
    _enusre_paths_are_all_files(file_specs.binaries)
    _ensure_path_names_are_unique(file_specs.binaries)

    _enusre_paths_are_all_files(file_specs.libraries)
    _ensure_path_names_are_unique(file_specs.libraries)

    _enusre_paths_are_all_directories(file_specs.includes)
    _ensure_path_names_are_unique(file_specs.includes)


def _enusre_paths_are_all_directories(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_dir():
            raise ValueError(f"Path '{path}' is not a directory.")


def _enusre_paths_are_all_files(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_file():
            raise ValueError(f"Path '{path}' is not a file.")


def _ensure_path_names_are_unique(files: list[Path]) -> None:
    """
    This function ensures that all the names in the list are unique.

    Example: The following two entries in the list would raise an exception:

      - /path_a/file
      - /path_b/file

    because the packaging logic will copy these files to the same location, e.g. the bin, lib or include folder.
    """
    counter = Counter([file.name for file in files])
    duplicates = {name for name, count in counter.items() if count > 1}
    if len(duplicates) > 0:
        raise ValueError(f"Duplicate file names found: {', '.join(duplicates)}")


def _copy_file_paths_to_target(file_paths: list[Path], target_path: Path) -> None:
    ensure_dir_exists(target_path)
    for file_path in file_paths:
        copy(file_path, target_path / file_path.name)


def _copy_dir_paths_to_target(dir_paths: list[Path], target_path: Path) -> None:
    ensure_dir_exists(target_path)
    for dir_path in dir_paths:
        copytree(dir_path, target_path / dir_path.name)


def _create_zip_archive(source_path: Path, output_path: Path):
    """
    Creates a zip file containing all the files and directories within source_dir.

    :param source_path: The directory whose contents are to be zipped.
    :param output_path: The name of the output zip file.
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in source_path.rglob("*"):
            zip_file.write(file, file.relative_to(source_path))
