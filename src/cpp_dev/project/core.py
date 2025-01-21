# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from textwrap import dedent

from cpp_dev.common.version import SemanticVersionWithOptionalParts
from cpp_dev.dependency.provider import Dependency, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier
from cpp_dev.dependency.types import DependencySpecifierParts, VersionSpecBound, VersionSpecBoundOperand

from .config import (
    DependencyType,
    ProjectConfig,
    create_project_config,
    load_project_config,
    store_project_config,
    update_dependencies,
)
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

    def add_package_dependency(self, deps: list[DependencySpecifier], dep_type: DependencyType) -> None:
        """Add package dependencies to the project for the given type."""
        refined_deps = _refine_package_dependencies(self._dependency_provider, deps)
        project_config = load_project_config(self.project_dir)
        update_dependencies(project_config, refined_deps, dep_type)
        dependency_hull = _obtain_dependency_hull(project_config, self._dependency_provider)

        store_project_config(self.project_dir, project_config)


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


def _add_default_cpd_dependencies(project: Project) -> None:
    project.add_package_dependency(
        [
            DependencySpecifier("llvm"),
            DependencySpecifier("gtest"),
        ],
        "cpd",
    )


DEFAULT_REPOSITORY = "official"


def _refine_package_dependencies(
    dep_provider: DependencyProvider, deps: list[DependencySpecifier]
) -> list[DependencySpecifier]:
    """Refine the package dependencies in case of defaults were chosen.

    The refinement includes (in order):
        o Default repository "official"
        o Latest resolved version in case of "latest"

    This step is performed to assure that package dependencies with "latest" do not get an older version
    than the latest one at the time of resolution. This is important in case a versions gets removed.
    """
    updated_deps = []
    for dep in deps:
        repository = dep.repository if dep.repository is not None else DEFAULT_REPOSITORY
        version_spec = dep.version_spec
        if dep.version_spec == "latest":
            available_versions = dep_provider.fetch_versions(repository, dep.name)
            if len(available_versions) == 0:
                raise ValueError(f"No available versions for package {dep.name} at repository {dep.repository}.")
            version_spec = [
                VersionSpecBound(
                    operand=VersionSpecBoundOperand.GREATER_THAN_OR_EQUAL,
                    version=SemanticVersionWithOptionalParts.from_semantic_version(available_versions[0]),
                )
            ]
        updated_deps.append(
            DependencySpecifier.from_parts(DependencySpecifierParts(repository, dep.name, version_spec))
        )
    return updated_deps


def _obtain_dependency_hull(project_config: ProjectConfig, dep_provider: DependencyProvider) -> list[Dependency]:
    """Obtain the dependency hull for the given project configuration."""
    return dep_provider.collect_dependency_hull(
        project_config.dependencies + project_config.dev_dependencies + project_config.cpd_dependencies
    )
