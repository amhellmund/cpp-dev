# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.project.setup import setup_project
from cpp_dev.project.types import SemanticVersion
from cpp_dev.project.utils import load_project_config


def test_setup_project(tmp_path):
    NAME = "test_package"
    VERSION = SemanticVersion("1.0.0")
    STD = "c++17"
    AUTHOR = "author"
    LICENSE = "license"
    DESCRIPTION = "description"

    project_dir = setup_project(
        NAME, VERSION, STD, AUTHOR, LICENSE, DESCRIPTION, parent_dir=tmp_path
    )

    assert project_dir.exists()
    assert project_dir == tmp_path / NAME

    assert (project_dir / "cpp-dev.yaml").exists()

    config = load_project_config(project_dir)
    assert config.name == NAME
    assert config.version == VERSION
    assert config.std == STD
    assert config.author == AUTHOR
    assert config.license == LICENSE
    assert config.description == DESCRIPTION
    assert len(config.dependencies) == 0
    assert len(config.dev_dependencies) == 0

    assert (project_dir / "include" / NAME / f"{NAME}.hpp").exists()
    assert (project_dir / "src" / f"{NAME}.cpp").exists()
    assert (project_dir / "src" / f"{NAME}.test.cpp").exists()

    assert (project_dir / ".env" / "bin").exists()
    assert (project_dir / ".env" / "lib").exists()
    assert (project_dir / ".env" / "include").exists()
    assert (project_dir / ".env" / ".link_index").exists()
