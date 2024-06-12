# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

import yaml
from pathlib import Path

from .types import ProjectConfig
from .constants import compose_project_config_file


def load_project_config(project_dir: Path) -> ProjectConfig:
    """
    Loads the package configuration from the specified package folder.
    """
    config_file = compose_project_config_file(project_dir)
    return ProjectConfig.model_validate(yaml.safe_load(config_file.read_text()))


def store_project_config(project_dir: Path, config: ProjectConfig) -> None:
    """
    Stores the package configuration in the specified package folder.
    """
    config_file = compose_project_config_file(project_dir)
    config_file.write_text(yaml.dump(config.model_dump()))
