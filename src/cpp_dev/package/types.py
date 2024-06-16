# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations
from pathlib import Path

from cpp_dev.common.types import PackageRef, SemanticVersion
from pydantic import BaseModel


PackageName = str


class PackageVersionDetails(BaseModel):
    dependencies: list[PackageRef]
    path: Path


class PackageSpecs(BaseModel):
    versions: dict[SemanticVersion, PackageVersionDetails]
    latest: SemanticVersion


class PackageIndex(BaseModel):
    repository: str
    packages: dict[PackageName, PackageSpecs]
