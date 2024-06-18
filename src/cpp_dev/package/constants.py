# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from cpp_dev.package.types import OperatingSystem, PackageRef


def compose_index_path(os: OperatingSystem, repository: str) -> Path:
    return Path("indexes") / os.compose_canonical_path() / f"{repository}.json"


def compose_package_path(os: OperatingSystem, ref: PackageRef) -> Path:
    repository, name, version = ref.unpack
    print(repository, name, version)
    return (
        Path("packages")
        / os.compose_canonical_path()
        / f"{repository}"
        / f"{name}-{version}.zip"
    )
