# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
import pytest

from cpp_dev.package.constants import compose_index_path, compose_package_path
from cpp_dev.package.types import OperatingSystem, PackageRef


@pytest.fixture
def test_os():
    return OperatingSystem(
        arch="x86_64",
        name="ubuntu",
        version="22.04",
    )


def test_compose_index_path(test_os: OperatingSystem) -> None:
    assert compose_index_path(test_os, "official") == Path(
        "indexes/x86_64-ubuntu-22.04/official.json"
    )


def test_compose_package_path(test_os: OperatingSystem) -> None:
    assert compose_package_path(test_os, PackageRef("official-package-1.0.0")) == (
        Path("packages/x86_64-ubuntu-22.04/official/package-1.0.0.zip")
    )
