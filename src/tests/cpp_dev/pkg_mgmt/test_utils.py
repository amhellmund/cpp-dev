# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from pathlib import Path
from cpp_dev.pkg_mgmt.types import PackageConfig
from cpp_dev.pkg_mgmt.utils import load_package_config, store_package_config

def test_roundtrip(tmp_path: Path):
    config_file = tmp_path
    
    config = PackageConfig(
        format_version=1,
        name="test",
        version="0.1.0",
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
    )

    store_package_config(config_file, config)
    loaded_config = load_package_config(config_file)

    assert loaded_config == config