# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from copy import deepcopy
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

from cpp_dev.common.types import CppStandard
from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.specifier import DependencySpecifier

from .path_composition import compose_project_config_file

###############################################################################
# Public API                                                                ###
###############################################################################

DependencyType = Literal["runtime", "dev", "cpd"]


class ProjectConfig(BaseModel):
    """A project configuration for a cpp-dev project."""

    name: str
    version: SemanticVersion
    std: CppStandard

    author: str | None
    license: str | None
    description: str | None

    # Public dependencies used by the project
    dependencies: list[DependencySpecifier]

    # Development dependencies used by the project while developing
    dev_dependencies: list[DependencySpecifier]

    # Cpp-Dev dependencies used by the tool itself. These dependencies can only be updated but not removed.
    cpd_dependencies: list[DependencySpecifier]

    def get_dependencies(self, dep_type: DependencyType) -> list[DependencySpecifier]:
        """Return the dependency list by type."""
        if dep_type == "runtime":
            return self.dependencies
        if dep_type == "dev":
            return self.dev_dependencies
        if dep_type == "cpd":
            return self.cpd_dependencies
        raise ValueError(f"Invalid dependency type requested: {dep_type}")


def create_project_config(
    project_dir: Path,
    project_config: ProjectConfig,
) -> None:
    """Create a package configuration file for the cpp-dev package.

    The configuration file is saved in the package folder.
    """
    store_project_config(project_dir, project_config)


def load_project_config(project_dir: Path) -> ProjectConfig:
    """Load the package configuration from the specified package folder."""
    config_file = compose_project_config_file(project_dir)
    return ProjectConfig.model_validate(yaml.safe_load(config_file.read_text()))


def store_project_config(project_dir: Path, config: ProjectConfig) -> None:
    """Store the package configuration in the specified package folder."""
    config_file = compose_project_config_file(project_dir)
    config_file.write_text(yaml.dump(config.model_dump()))


def update_dependencies(
    project_config: ProjectConfig,
    deps: list[DependencySpecifier],
    dep_type: DependencyType,
) -> ProjectConfig:
    """Update the dependency in the project configuration."""
    updated_config = deepcopy(project_config)
    _update_or_add_dependency_entries(updated_config.get_dependencies(dep_type), deps)
    return updated_config


###############################################################################
# Implementation                                                            ###
###############################################################################


def _update_or_add_dependency_entries(
    existing_deps: list[DependencySpecifier],
    new_deps: list[DependencySpecifier],
) -> None:
    repo_and_name_to_index_mapping = {
        (entry.parts.repository, entry.parts.name): idx for idx, entry in enumerate(existing_deps)
    }
    for dep in new_deps:
        key = (dep.parts.repository, dep.parts.name)
        if key in repo_and_name_to_index_mapping:
            idx = repo_and_name_to_index_mapping[key]
            existing_deps[idx] = dep
        else:
            existing_deps.append(dep)
