# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.project.lockfile import (
    LockedDependencies,
    LockedPackageDependency,
    create_initial_lock_file,
    load_lock_file,
    store_lock_file,
)
from cpp_dev.project.path_composition import compose_project_lock_file


@pytest.fixture
def locked_dependencies() -> LockedDependencies:
    return LockedDependencies(
        packages=[LockedPackageDependency(repository="official", name="cpd", version=SemanticVersion("1.0.0"))]
    )


def test_create_initial_lock_file(tmp_path: Path) -> None:
    project_lock_file_path = compose_project_lock_file(tmp_path)
    assert not project_lock_file_path.exists()
    create_initial_lock_file(tmp_path)
    assert project_lock_file_path.exists()
    loaded_locked_dependencies = load_lock_file(tmp_path)
    assert len(loaded_locked_dependencies.packages) == 0


def test_lock_file_round_trip(tmp_path: Path, locked_dependencies: LockedDependencies) -> None:
    project_lock_file_path = compose_project_lock_file(tmp_path)
    assert not project_lock_file_path.exists()
    store_lock_file(tmp_path, locked_dependencies)
    assert project_lock_file_path.exists()
    loaded_locked_dependencies = load_lock_file(tmp_path)
    assert loaded_locked_dependencies == locked_dependencies
