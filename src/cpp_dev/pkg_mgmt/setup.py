# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from textwrap import dedent
import yaml
from pathlib import Path
from typing import Optional

from cpp_dev.common.types import CppStandard

from .types import PackageConfig, SemanticVersion
from .constants import CONFIG_FILE_FORMAT_VERSION, CONFIG_FILE_NAME, INCLUDE_FOLDER, SOURCE_FOLDER
from .utils import store_package_config

def setup_package (
    name: str,
    version: SemanticVersion,
    std: CppStandard,
    author: Optional[str],
    license: Optional[str],
    description: Optional[str],
    parent_dir: Path = Path.cwd()
) -> Path:
    """
    Creates a new cpp-dev package in the specified parent directory.

    The path to the new package directory is returned.
    """
    package_folder = _validate_package_folder(parent_dir, name)
    _create_package_config(package_folder, name, version, std, author, license, description)
    _create_project_files(package_folder, name)
    return package_folder


def _validate_package_folder(parent_dir: Path, name: str) -> Path:
    """
    Checks and validates if the package folder does not yet exist.
    """
    package_folder = parent_dir / name
    if package_folder.exists():
        raise ValueError(f"Package folder {package_folder} already exists.")
    package_folder.mkdir(parents=True)
    return package_folder


def _create_package_config(
    package_folder: Path,
    name: str,
    version: SemanticVersion,
    std: CppStandard,
    author: Optional[str],
    license: Optional[str],
    description: Optional[str]
) -> None:
    """
    Creates a package configuration file for the cpp-dev package.

    The configuration file is saved in the package folder.
    """
    store_package_config(
        package_folder,
        PackageConfig(
            format_version=CONFIG_FILE_FORMAT_VERSION,
            name=name,
            version=version,
            std=std,
            author=author,
            license=license,
            description=description,
            dependencies=[]
        )
    )

def _create_project_files(package_folder: Path, name: str) -> None:
    """
    Creates the necessary project files for the cpp-dev package.
    """
    include_file = package_folder / INCLUDE_FOLDER / name / f"{name}.hpp"
    include_file.parent.mkdir(parents=True)
    include_file.write_text(
        dedent(
            f"""\
            #pragma once

            namespace {name} {{
                int api();
            }}
            """
        )
    )

    source_file = package_folder / SOURCE_FOLDER / f"{name}.cpp"
    source_file.parent.mkdir(parents=True)
    source_file.write_text(
        dedent(
            f"""\
            #include "{name}/{name}.hpp"

            int {name}::api() {{
                return 42;
            }}
            """
        )
    )

    test_file = package_folder / SOURCE_FOLDER / f"{name}.test.cpp"
    test_file.write_text(
        dedent(
            f"""\
            #include <gtest/gtest.h>
            #include "{name}/{name}.hpp"
            

            TEST({name}, api) {{
                EXPECT_EQ({name}::api(), 42);
            }}
            """
        )
    )