# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

from cpp_dev.project.config import load_project_config
from cpp_dev.project.constants import compose_project_config_file, compose_project_lock_file
from cpp_dev.project.lockfile import load_lock_file
from cpp_dev.project.management import setup_project
from cpp_dev.project.types import ProjectConfig, SemanticVersion


def test_setup_project(tmp_path: Path) -> None:
    project_config = ProjectConfig(
        name="test_package",
        version=SemanticVersion("1.0.0"),
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
        dev_dependencies=[],
        cpd_dependencies=[],
    )

    project_dir = setup_project(project_config, parent_dir=tmp_path)

    assert project_dir.exists()
    assert project_dir == tmp_path / project_config.name

    assert compose_project_config_file(project_dir).exists()

    config = load_project_config(project_dir)
    assert config == project_config

    assert len(config.dependencies) == 0
    assert len(config.dev_dependencies) == 0
    assert len(config.cpd_dependencies) == 0

    assert compose_project_lock_file(project_dir).exists()
    locked_dependencies = load_lock_file(project_dir)
    assert len(locked_dependencies.packages) == 0

    assert (project_dir / "include" / project_config.name / f"{project_config.name}.hpp").exists()
    assert (project_dir / "src" / f"{project_config.name}.cpp").exists()
    assert (project_dir / "src" / f"{project_config.name}.test.cpp").exists()
