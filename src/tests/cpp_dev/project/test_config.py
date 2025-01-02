# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from typing import NamedTuple

import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.specifier import DependencySpecifier
from cpp_dev.project.config import (
    DependencyType,
    ProjectConfig,
    create_project_config,
    load_project_config,
    update_dependencies,
)
from cpp_dev.project.constants import compose_project_config_file


@pytest.fixture
def project_config() -> ProjectConfig:
    return ProjectConfig(
        name="test",
        version=SemanticVersion("0.1.0"),
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
        dev_dependencies=[DependencySpecifier("cpd")],
        cpd_dependencies=[DependencySpecifier("cpd"), DependencySpecifier("cpd2")],
    )


def test_create_project_config(tmp_path: Path, project_config: ProjectConfig) -> None:
    project_config_file_path = compose_project_config_file(tmp_path)
    assert not project_config_file_path.exists()
    create_project_config(tmp_path, project_config)
    assert project_config_file_path.exists()
    loaded_config = load_project_config(tmp_path)
    assert loaded_config == project_config


class ProjectSetup(NamedTuple):
    project_dir: Path
    project_config: ProjectConfig


@pytest.fixture
def project_setup(tmp_path: Path, project_config: ProjectConfig) -> ProjectSetup:
    create_project_config(tmp_path, project_config)
    return ProjectSetup(tmp_path, project_config)


@pytest.mark.parametrize(
    ("dep_type", "new_deps", "expected_deps", "unchanged_dep_types"),
    [
        ("runtime", [DependencySpecifier("cpd")], [DependencySpecifier("cpd")], ["dev", "cpd"]),
        ("dev", [DependencySpecifier("cpd[2.0.0]")], [DependencySpecifier("cpd[2.0.0]")], ["runtime", "cpd"]),
        (
            "cpd",
            [DependencySpecifier("cpd"), DependencySpecifier("cpd3")],
            [DependencySpecifier("cpd"), DependencySpecifier("cpd2"), DependencySpecifier("cpd3")],
            ["runtime", "dev"],
        ),
    ],
)
def test_update_dependencies(
    project_setup: ProjectSetup,
    dep_type: DependencyType,
    new_deps: list[DependencySpecifier],
    expected_deps: list[DependencySpecifier],
    unchanged_dep_types: list[DependencyType],
) -> None:
    new_config = update_dependencies(project_setup.project_config, new_deps, dep_type)

    assert new_config.get_dependencies(dep_type) == expected_deps

    for unchanged_type in unchanged_dep_types:
        assert new_config.get_dependencies(unchanged_type) == project_setup.project_config.get_dependencies(
            unchanged_type
        )
