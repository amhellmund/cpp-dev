# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from textwrap import dedent
from typing import get_args

from cpp_dev.conan.package import compute_dependency_graph

from ..dependency.types import PackageDependency
from .config import create_project_config, load_project_config, update_dependencies
from .dependency.utils import refine_package_dependencies
from .lockfile import create_initial_lock_file
from .path_composition import compose_include_file, compose_source_file
from .types import DependencyType, ProjectConfig

###############################################################################
# Public API                                                                ###
###############################################################################


def add_package_dependency(project_dir: Path, deps: list[PackageDependency], dep_type: DependencyType) -> None:
    """Add package dependencies to the project for the given type."""
    refined_deps = refine_package_dependencies(deps)
    project_config = load_project_config(project_dir)
    updated_config = update_dependencies(project_config, refined_deps, dep_type)
    _collect_dependency_graph(updated_config)


###############################################################################
# Implementation                                                            ###
###############################################################################


def _collect_dependency_graph(project_config: ProjectConfig) -> None:
    all_package_deps = [
        dep for dep_type in get_args(DependencyType) for dep in project_config.get_dependencies(dep_type)
    ]
    compute_dependency_graph(all_package_deps)
