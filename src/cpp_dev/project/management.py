# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from textwrap import dedent
from typing import get_args

from cpp_dev.conan.package import compute_dependency_graph

from ..dependency.types import PackageDependency
from .config import create_project_config, load_project_config, update_dependencies
from .constants import compose_include_file, compose_source_file
from .dependency.utils import refine_package_dependencies
from .lockfile import create_initial_lock_file
from .types import DependencyType, ProjectConfig

###############################################################################
# Public API                                                                ###
###############################################################################


def setup_project(
    project_config: ProjectConfig,
    parent_dir: Path | None = None,
) -> Path:
    """Create a new cpp-dev project in the specified parent directory.

    The path to the new project directory is returned.
    """
    project_dir = _validate_project_dir(parent_dir, project_config.name)
    create_project_config(project_dir, project_config)
    create_initial_lock_file(project_dir)
    _add_default_cpd_dependencies(project_dir)
    _create_project_files(project_dir, project_config.name)
    return project_dir


def add_package_dependency(project_dir: Path, deps: list[PackageDependency], dep_type: DependencyType) -> None:
    """Add package dependencies to the project for the given type."""
    refined_deps = refine_package_dependencies(deps)
    project_config = load_project_config(project_dir)
    updated_config = update_dependencies(project_config, refined_deps, dep_type)
    _collect_dependency_graph(updated_config)


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


def _add_default_cpd_dependencies(project_dir: Path) -> None:
    add_package_dependency(project_dir, [PackageDependency("llvm"), PackageDependency("gtest")], "cpd")


def _collect_dependency_graph(project_config: ProjectConfig) -> None:
    all_package_deps = [
        dep for dep_type in get_args(DependencyType) for dep in project_config.get_dependencies(dep_type)
    ]
    compute_dependency_graph(all_package_deps)


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
