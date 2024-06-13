# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License


from __future__ import annotations

from cpp_dev.common.types import PackageRef, SemanticVersion
from pydantic import BaseModel


class PackageSpecs(BaseModel):
    dependencies: list[PackageRef]
    path: str


class Package(BaseModel):
    name: str
    versions: dict[SemanticVersion, PackageSpecs]
    latest: SemanticVersion


class PackageIndex(BaseModel):
    repository: str
    packages: list[Package]
