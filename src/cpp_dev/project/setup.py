# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
from textwrap import dedent

from cpp_dev.project.lockfile import create_initial_lock_file

from .config import create_project_config
from .constants import compose_include_file, compose_source_file
from .types import ProjectConfig

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
    _create_project_files(project_dir, project_config.name)
    return project_dir


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
