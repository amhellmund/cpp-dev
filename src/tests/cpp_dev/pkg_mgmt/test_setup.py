# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from cpp_dev.pkg_mgmt.setup import setup_package
from cpp_dev.pkg_mgmt.types import SemanticVersion
from cpp_dev.pkg_mgmt.utils import load_package_config


def test_setup_package(tmp_path):
    NAME = "test_package"
    VERSION = SemanticVersion("1.0.0")
    STD = "c++17"
    AUTHOR = "author"
    LICENSE = "license"
    DESCRIPTION = "description"

    package_dir = setup_package(
        NAME, VERSION, STD, AUTHOR, LICENSE, DESCRIPTION, parent_dir=tmp_path
    )

    assert package_dir.exists()
    assert package_dir == tmp_path / NAME

    assert (package_dir / "cpp-dev.yaml").exists()

    config = load_package_config(package_dir)
    assert config.name == NAME
    assert config.version == VERSION
    assert config.std == STD
    assert config.author == AUTHOR
    assert config.license == LICENSE
    assert config.description == DESCRIPTION
    assert len(config.dependencies) == 0
    assert len(config.dev_dependencies) == 0

    assert (package_dir / "include" / NAME / f"{NAME}.hpp").exists()
    assert (package_dir / "src" / f"{NAME}.cpp").exists()
    assert (package_dir / "src" / f"{NAME}.test.cpp").exists()

    assert (package_dir / ".env" / "bin").exists()
    assert (package_dir / ".env" / "lib").exists()
    assert (package_dir / ".env" / "include").exists()
    assert (package_dir / ".env" / ".link_index").exists()
