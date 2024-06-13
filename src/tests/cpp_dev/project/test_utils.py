# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from pathlib import Path
from cpp_dev.project.types import ProjectConfig
from cpp_dev.project.utils import load_project_config, store_project_config


def test_roundtrip(tmp_path: Path):
    config_file = tmp_path

    config = ProjectConfig(
        name="test",
        version="0.1.0",
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
        dev_dependencies=[],
    )

    store_project_config(config_file, config)
    loaded_config = load_project_config(config_file)

    assert loaded_config == config
