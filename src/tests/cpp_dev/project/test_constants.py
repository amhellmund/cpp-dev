# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import pytest
from pathlib import Path

from cpp_dev.project.constants import (
    compose_project_config_file,
    compose_include_file,
    compose_source_file,
    compose_env_dir,
    compose_env_bin_dir,
    compose_env_lib_dir,
    compose_env_include_dir,
    compose_env_link_index_dir,
)


@pytest.fixture
def test_project_dir() -> Path:
    return Path("project")


def test_compose_project_config_file(test_project_dir: Path) -> None:
    assert compose_project_config_file(test_project_dir) == Path("project/cpp-dev.yaml")


def test_compose_include_file(test_project_dir: Path) -> None:
    assert compose_include_file(test_project_dir, "test", "test.hpp") == Path(
        "project/include/test/test.hpp"
    )


def test_compose_source_file(test_project_dir: Path) -> None:
    assert compose_source_file(test_project_dir, "test.cpp") == Path(
        "project/src/test.cpp"
    )


def test_compose_env_dir(test_project_dir: Path) -> None:
    assert compose_env_dir(test_project_dir) == Path("project/.env")


def test_compose_env_bin_dir(test_project_dir: Path) -> None:
    assert compose_env_bin_dir(test_project_dir / ".env") == Path("project/.env/bin")


def test_compose_env_lib_dir(test_project_dir: Path) -> None:
    assert compose_env_lib_dir(test_project_dir / ".env") == Path("project/.env/lib")


def test_compose_env_include_dir(test_project_dir: Path) -> None:
    assert compose_env_include_dir(test_project_dir / ".env") == Path(
        "project/.env/include"
    )


def test_compose_env_index_dir(test_project_dir: Path) -> None:
    assert compose_env_link_index_dir(test_project_dir / ".env") == Path(
        "project/.env/.link_index"
    )
