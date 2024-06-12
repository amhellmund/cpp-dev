# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from textwrap import dedent
from pathlib import Path
from typing import Optional

from cpp_dev.common.types import CppStandard

from .types import ProjectConfig, SemanticVersion
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
from .utils import store_project_config


def setup_project(
    name: str,
    version: SemanticVersion,
    std: CppStandard,
    author: Optional[str],
    license: Optional[str],
    description: Optional[str],
    parent_dir: Path = Path.cwd(),
) -> Path:
    """
    Creates a new cpp-dev project in the specified parent directory.

    The path to the new project directory is returned.
    """
    project_dir = _validate_project_dir(parent_dir, name)
    _create_project_config(
        project_dir, name, version, std, author, license, description
    )
    _create_project_files(project_dir, name)
    return project_dir


def _validate_project_dir(parent_dir: Path, name: str) -> Path:
    """
    Checks and validates if the project directory does not yet exist.
    """
    project_dir = parent_dir / name
    if project_dir.exists():
        raise ValueError(f"Project directory {project_dir} already exists.")
    project_dir.mkdir(parents=True)
    return project_dir


def _create_project_config(
    project_dir: Path,
    name: str,
    version: SemanticVersion,
    std: CppStandard,
    author: Optional[str],
    license: Optional[str],
    description: Optional[str],
) -> ProjectConfig:
    """
    Creates a package configuration file for the cpp-dev package.

    The configuration file is saved in the package folder.
    """
    config = ProjectConfig(
        format_version=CONFIG_FILE_FORMAT_VERSION,
        name=name,
        version=version,
        std=std,
        author=author,
        license=license,
        description=description,
        dependencies=[],
        dev_dependencies=[],
    )
    store_project_config(project_dir, config)
    return config


def _create_project_files(project_dir: Path, name: str) -> None:
    """
    Creates the necessary project files for the cpp-dev package.
    """
    _create_library_include_file(project_dir, name)
    _create_library_source_file(project_dir, name)
    _create_library_test_file(project_dir, name)
    _create_env(project_dir)


def _create_library_include_file(project_dir: Path, name: str) -> None:
    include_file = compose_include_file(project_dir, name, f"{name}.hpp")
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


def _create_library_source_file(project_dir: Path, name: str) -> None:
    source_file = compose_source_file(project_dir, f"{name}.cpp")
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


def _create_library_test_file(project_dir: Path, name: str) -> None:
    test_file = compose_source_file(project_dir, f"{name}.test.cpp")
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


def _create_env(project_dir: Path) -> None:
    env_dir = compose_env_dir(project_dir)
    env_dir.mkdir(parents=True)

    compose_env_bin_dir(env_dir).mkdir(parents=True)
    compose_env_lib_dir(env_dir).mkdir(parents=True)
    compose_env_include_dir(env_dir).mkdir(parents=True)

    compose_env_link_index_dir(env_dir).mkdir(parents=True)
