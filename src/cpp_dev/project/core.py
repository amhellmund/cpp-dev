# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from textwrap import dedent

from cpp_dev.dependency.provider import DependencyProvider

from .config import ProjectConfig, create_project_config
from .lockfile import create_initial_lock_file
from .path_composition import compose_include_file, compose_source_file

###############################################################################
# Public API                                                                ###
###############################################################################


class Project:
    """Main interface for managing cpp-dev projects."""

    def __init__(self, project_dir: Path, dependency_provider: DependencyProvider) -> None:
        self._project_dir = project_dir
        self._dependency_provider = dependency_provider

    @property
    def project_dir(self) -> Path:
        """Return the path to the project directory."""
        return self._project_dir


def setup_project(
    project_config: ProjectConfig,
    dependency_provider: DependencyProvider,
    parent_dir: Path | None = None,
) -> Project:
    """Create a new cpp-dev project in the specified parent directory.

    The path to the new project directory is returned.
    """
    project_dir = _validate_project_dir(parent_dir, project_config.name)
    create_project_config(project_dir, project_config)
    create_initial_lock_file(project_dir)
    _create_project_files(project_dir, project_config.name)

    project = Project(project_dir, dependency_provider)
    _add_default_cpd_dependencies(project)

    return project


###############################################################################
# Implementation                                                            ###
###############################################################################


def _validate_project_dir(parent_dir: Path | None, name: str) -> Path:
    """Check and validate if the project directory does not yet exist."""
    if parent_dir is None:
        parent_dir = Path.cwd()
    project_dir = parent_dir / name
    if project_dir.exists():
        raise ValueError(f"Project directory {project_dir} already exists.")
    project_dir.mkdir(parents=True)
    return project_dir


def _create_project_files(project_dir: Path, name: str) -> None:
    """Create the necessary project files for the cpp-dev package."""
    _create_library_include_file(project_dir, name)
    _create_library_source_file(project_dir, name)
    _create_library_test_file(project_dir, name)


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
            """,
        ),
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
            """,
        ),
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
            """,
        ),
    )


def _add_default_cpd_dependencies(project_dir: Path) -> None:
    # add_package_dependency(project_dir, [PackageDependency("llvm"), PackageDependency("gtest")], "cpd")  # noqa: ERA001
    ...
