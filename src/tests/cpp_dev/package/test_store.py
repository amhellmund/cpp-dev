# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from pathlib import Path
from cpp_dev.common.file_io import FileIOLocal
from cpp_dev.common.types import SemanticVersion
from cpp_dev.package.store import PackageStore, compose_index_path, compose_package_path
from cpp_dev.package.types import OperatingSystem, PackageIndex, PackageRef


@pytest.fixture
def test_os():
    return OperatingSystem(
        arch="x86_64",
        name="os",
        version="version",
    )


@pytest.fixture()
def package_store(test_os) -> PackageStore:
    return PackageStore(
        file_io=FileIOLocal(Path(__file__).parent / "data"),
        os=test_os,
    )


def test_artifact_io_index(package_store: PackageStore):
    index_content = package_store.get_index("repo")
    index = PackageIndex.model_validate_json(index_content)

    assert index.repository == "repo"
    assert len(index.packages) == 1

    assert "simple_package" in index.packages
    specs = index.packages["simple_package"]
    assert len(specs.versions) == 1

    assert SemanticVersion("1.0.0") in specs.versions
    version = specs.versions[SemanticVersion("1.0.0")]
    assert version.dependencies == []
    assert version.sha1sum == "sha1sum"


def test_artifact_io_package(package_store: PackageStore):
    package_content = package_store.get_package_file(
        PackageRef("repo-simple_package-1.0.0")
    )
    assert package_content == b"package-content"


def test_compose_index_path(test_os: OperatingSystem) -> None:
    assert compose_index_path(test_os, "official") == Path(
        "indexes/x86_64-os-version/official.json"
    )


def test_compose_package_path(test_os: OperatingSystem) -> None:
    assert compose_package_path(test_os, PackageRef("official-package-1.0.0")) == (
        Path("packages/x86_64-os-version/official/package-1.0.0.zip")
    )
