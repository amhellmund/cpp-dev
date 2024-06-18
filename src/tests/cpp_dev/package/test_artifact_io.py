# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from pathlib import Path
from cpp_dev.common.file_io import FileIOLocal
from cpp_dev.common.types import SemanticVersion
from cpp_dev.package.artifact_io import ArtifactIO
from cpp_dev.package.types import OperatingSystem, PackageIndex, PackageRef


@pytest.fixture()
def artifact_io_store() -> ArtifactIO:
    return ArtifactIO(
        file_io=FileIOLocal(Path(__file__).parent / "data"),
        os=OperatingSystem(
            arch="x86_64",
            name="os",
            version="version",
        ),
    )


def test_artifact_io_index(artifact_io_store: ArtifactIO):
    index_content = artifact_io_store.get_index("repo")
    index = PackageIndex.model_validate_json(index_content)

    assert index.repository == "repo"
    assert len(index.packages) == 1

    assert "simple_package" in index.packages
    specs = index.packages["simple_package"]
    assert len(specs.versions) == 1

    assert SemanticVersion("1.0.0") in specs.versions
    version = specs.versions[SemanticVersion("1.0.0")]
    assert version.dependencies == []


def test_artifact_io_package(artifact_io_store: ArtifactIO):
    package_content = artifact_io_store.get_package_file(
        PackageRef("repo-simple_package-1.0.0")
    )
    assert package_content == b"package-content"
