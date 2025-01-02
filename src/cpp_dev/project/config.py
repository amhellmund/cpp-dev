# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from copy import deepcopy
from pathlib import Path

import yaml

from ..dependency.types import PackageDependency
from .constants import compose_project_config_file
from .types import DependencyType, ProjectConfig

###############################################################################
# Public API                                                                ###
###############################################################################


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
    deps: list[PackageDependency],
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
    existing_deps: list[PackageDependency],
    new_deps: list[PackageDependency],
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
