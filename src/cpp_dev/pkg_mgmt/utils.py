# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

import yaml
from pathlib import Path

from .types import PackageConfig
from .constants import CONFIG_FILE_NAME

def load_package_config(package_folder: Path) -> PackageConfig:
    """
    Loads the package configuration from the specified package folder.
    """
    config_file = package_folder / CONFIG_FILE_NAME
    return PackageConfig.model_validate(
        yaml.safe_load(config_file.read_text())
    )

def store_package_config(package_folder: Path, config: PackageConfig) -> None:
    """
    Stores the package configuration in the specified package folder.
    """
    config_file = package_folder / CONFIG_FILE_NAME
    config_file.write_text(yaml.dump(config.model_dump()))