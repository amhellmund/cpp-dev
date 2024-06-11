# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

import yaml
from pathlib import Path

from .types import PackageConfig
from .constants import compose_package_config_file


def load_package_config(package_dir: Path) -> PackageConfig:
    """
    Loads the package configuration from the specified package folder.
    """
    config_file = compose_package_config_file(package_dir)
    return PackageConfig.model_validate(yaml.safe_load(config_file.read_text()))


def store_package_config(package_dir: Path, config: PackageConfig) -> None:
    """
    Stores the package configuration in the specified package folder.
    """
    config_file = compose_package_config_file(package_dir)
    config_file.write_text(yaml.dump(config.model_dump()))
