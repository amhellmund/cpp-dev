# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

from cpp_dev.common.types import SemanticVersion
from cpp_dev.project.types import ProjectConfig
from cpp_dev.project.utils import load_project_config, store_project_config


def test_roundtrip(tmp_path: Path) -> None:
    config_file = tmp_path

    config = ProjectConfig(
        name="test",
        version=SemanticVersion("0.1.0"),
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
        dev_dependencies=[],
        cpd_dependencies=[],
    )

    store_project_config(config_file, config)
    loaded_config = load_project_config(config_file)

    assert loaded_config == config
