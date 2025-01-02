# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

import pytest

from cpp_dev.project.path_composition import (
    compose_include_file,
    compose_project_config_file,
    compose_project_lock_file,
    compose_source_file,
)


@pytest.fixture
def test_project_dir() -> Path:
    return Path("project")


def test_compose_project_config_file(test_project_dir: Path) -> None:
    assert compose_project_config_file(test_project_dir) == Path("project/cpp-dev.yaml")


def test_compose_project_lock_file(test_project_dir: Path) -> None:
    assert compose_project_lock_file(test_project_dir) == Path("project/cpp-dev.lock")


def test_compose_include_file(test_project_dir: Path) -> None:
    assert compose_include_file(test_project_dir, "test", "test.hpp") == Path("project/include/test/test.hpp")


def test_compose_source_file(test_project_dir: Path) -> None:
    assert compose_source_file(test_project_dir, "test.cpp") == Path("project/src/test.cpp")
    assert compose_include_file(test_project_dir, "test", "test.hpp") == Path("project/include/test/test.hpp")
