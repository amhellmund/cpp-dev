# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from copy import deepcopy
from pathlib import Path
from typing import get_args

from cpp_dev.dependency.specifier import DependencySpecifier

from .config import load_project_config, update_dependencies
from .types import DependencyType, ProjectConfig

###############################################################################
# Public API                                                                ###
###############################################################################


def add_package_dependency(project_dir: Path, deps: list[DependencySpecifier], dep_type: DependencyType) -> None:
    """Add package dependencies to the project for the given type."""
    refined_deps = _refine_package_dependencies(deps)
    project_config = load_project_config(project_dir)
    updated_config = update_dependencies(project_config, refined_deps, dep_type)
    _collect_dependency_graph(updated_config)


###############################################################################
# Implementation                                                            ###
###############################################################################


def _collect_dependency_graph(project_config: ProjectConfig) -> None: ...


DEFAULT_REPOSITORY = "official"


def _refine_package_dependencies(deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
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
            available_versions = get_available_versions(dep.repository, dep.name)
            if len(available_versions) == 0:
                raise ValueError(f"No available versions for package {parts.name} at repository {parts.repository}.")
            parts.version_spec = [
                VersionSpecBound(
                    operand=VersionSpecBoundOperand.GREATER_THAN_OR_EQUAL,
                    version=SemanticVersionWithOptionalParts.from_semantic_version(available_versions[0]),
                )
            ]
        updated_deps.append(PackageDependency.from_parts(parts))
    return updated_deps
