# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

import yaml
from pydantic import BaseModel

from cpp_dev.common.types import SemanticVersion
from cpp_dev.project.path_composition import compose_project_lock_file

###############################################################################
# Public API                                                                ###
###############################################################################


class LockedPackageDependency(BaseModel):
    """Package dependency inside a lock file."""

    repository: str
    name: str
    version: SemanticVersion


class LockedDependencies(BaseModel):
    """Lock file with fixed package dependencies."""

    packages: list[LockedPackageDependency]


def create_initial_lock_file(project_dir: Path) -> None:
    """Create the lock file."""
    store_lock_file(project_dir, LockedDependencies(packages=[]))


def store_lock_file(project_dir: Path, locked_dependencies: LockedDependencies) -> None:
    """Write the locked dependencies to file."""
    lock_file = compose_project_lock_file(project_dir)
    lock_file.write_text(yaml.dump(locked_dependencies.model_dump()))


def load_lock_file(project_dir: Path) -> LockedDependencies:
    """Read the locked dependencies from file."""
    lock_file = compose_project_lock_file(project_dir)
    return LockedDependencies.model_validate(yaml.safe_load(lock_file.read_text()))
