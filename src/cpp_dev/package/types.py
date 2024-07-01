# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from cpp_dev.common.types import SemanticVersion
from pydantic import BaseModel, RootModel, model_validator

from cpp_dev.common.utils import is_valid_name


@dataclass
class OperatingSystem:
    name: str
    version: str
    arch: Literal["x86_64"]

    def compose_canonical_path(self) -> Path:
        return f"{self.arch}-{self.name}-{self.version}"


type PackageName = str


class PackageVersionInfo(BaseModel):
    dependencies: list[PackageRef]
    sha1sum: str


class PackageInfo(BaseModel):
    versions: dict[SemanticVersion, PackageVersionInfo]


class PackageIndex(BaseModel):
    repository: str
    packages: dict[PackageName, PackageInfo]


class PackageFileSpecs(BaseModel):
    binaries: list[Path]
    libraries: list[Path]
    includes: list[Path]


class PackageRef(RootModel):
    root: str

    @property
    def unpack(self) -> tuple[str, str, SemanticVersion]:
        """
        Unpacks the package reference into its components:

        Returns: repository, package-name, version
        """
        components = self.root.split("-")
        print(components)
        repository, name, version = components
        return repository, name, SemanticVersion(version)

    @model_validator(mode="after")
    def validate_version(self) -> PackageRef:
        components = self.root.split("-")
        if len(components) != 3:
            raise ValueError(
                f"Invalid package ref: got {self.root}, expected <repository>.<package>.<semantic-version>"
            )

        if not is_valid_name(components[0]):
            raise ValueError(f"Invalid repository name: got {components[0]}")
        if not is_valid_name(components[1]):
            raise ValueError(f"Invalid package name: got {components[1]}")
        if not SemanticVersion.is_valid(components[2]):
            raise ValueError(f"Invalid semantic version: got {components[2]}")

        return self

    def __eq__(self, other: SemanticVersion) -> bool:
        return self.root == other.root

    def __hash__(self) -> int:
        return hash(self.root)
