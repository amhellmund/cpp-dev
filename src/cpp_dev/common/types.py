# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import RootModel, model_validator

from .utils import is_valid_name


CppStandard = Literal["c++11", "c++14", "c++17", "c++20", "c++23"]


@dataclass
class OperatingSystemDistribution:
    name: str
    version: str


class SemanticVersion(RootModel):
    root: str

    @staticmethod
    def is_valid(raw: str) -> bool:
        components = raw.split(".")
        if len(components) != 3:
            return False
        try:
            major, minor, patch = tuple(map(int, components))
        except ValueError:
            return False
        return major >= 0 and minor >= 0 and patch >= 0

    @model_validator(mode="after")
    def validate_version(self) -> SemanticVersion:
        if not self.is_valid(self.root):
            raise ValueError(
                f"Invalid semantic version string: got {self.root}, expected <major>.<minor>.<patch>."
                "Each version component must be positive."
            )
        return self

    def __eq__(self, other: SemanticVersion) -> bool:
        return self.root == other.root

    def __hash__(self) -> int:
        return hash(self.root)


class PackageRef(RootModel):
    root: str

    @property
    def unpack(self) -> tuple[str, str, SemanticVersion]:
        components = self.root.split("-")
        return components[0], components[1], SemanticVersion(components[2])

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
