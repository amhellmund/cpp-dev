# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from textwrap import dedent
from pathlib import Path
from typing import Optional

from cpp_dev.common.types import CppStandard

from .types import PackageConfig, SemanticVersion
from .constants import (
    CONFIG_FILE_FORMAT_VERSION,
    compose_env_bin_dir,
    compose_env_dir,
    compose_env_link_index_dir,
    compose_env_include_dir,
    compose_env_lib_dir,
    compose_include_file,
    compose_source_file,
)
from .utils import store_package_config


def setup_package(
    name: str,
    version: SemanticVersion,
    std: CppStandard,
    author: Optional[str],
    license: Optional[str],
    description: Optional[str],
    parent_dir: Path = Path.cwd(),
) -> Path:
    """
    Creates a new cpp-dev package in the specified parent directory.

    The path to the new package directory is returned.
    """
    package_folder = _validate_package_folder(parent_dir, name)
    _create_package_config(
        package_folder, name, version, std, author, license, description
    )
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
    description: Optional[str],
) -> PackageConfig:
    """
    Creates a package configuration file for the cpp-dev package.

    The configuration file is saved in the package folder.
    """
    config = PackageConfig(
        format_version=CONFIG_FILE_FORMAT_VERSION,
        name=name,
        version=version,
        std=std,
        author=author,
        license=license,
        description=description,
        dependencies=[],
    )
    store_package_config(package_folder, config)
    return config


def _create_project_files(package_dir: Path, name: str) -> None:
    """
    Creates the necessary project files for the cpp-dev package.
    """
    _create_library_include_file(package_dir, name)
    _create_library_source_file(package_dir, name)
    _create_library_test_file(package_dir, name)
    _create_env(package_dir)


def _create_library_include_file(package_dir: Path, name: str) -> None:
    include_file = compose_include_file(package_dir, name, f"{name}.hpp")
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


def _create_library_source_file(package_dir: Path, name: str) -> None:
    source_file = compose_source_file(package_dir, f"{name}.cpp")
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


def _create_library_test_file(package_dir: Path, name: str) -> None:
    test_file = compose_source_file(package_dir, f"{name}.test.cpp")
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


def _create_env(package_dir: Path) -> None:
    env_dir = compose_env_dir(package_dir)
    env_dir.mkdir(parents=True)

    compose_env_bin_dir(env_dir).mkdir(parents=True)
    compose_env_lib_dir(env_dir).mkdir(parents=True)
    compose_env_include_dir(env_dir).mkdir(parents=True)

    compose_env_link_index_dir(env_dir).mkdir(parents=True)
