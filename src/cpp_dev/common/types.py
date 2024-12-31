# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import RootModel, model_validator

###############################################################################
# Public API                                                                ###
###############################################################################

CppStandard = Literal["c++11", "c++14", "c++17", "c++20", "c++23"]


@dataclass
class SemanticVersionParts:
    """The semantic version components."""

    major: int
    minor: int
    patch: int

    def __lt__(self, other: SemanticVersionParts) -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)


class SemanticVersion(RootModel):
    """A semantic version string restricted to the <major>.<minor>.<patch> format.

    For details on semantic versioning, see https://semver.org/.
    """

    root: str

    @staticmethod
    def is_valid(raw: str) -> bool:
        """Check if a string is a valid semantic version."""
        components = raw.split(".")
        if len(components) != 3:
            return False
        try:
            major, minor, patch = tuple(map(int, components))
        except ValueError:
            return False
        return major >= 0 and minor >= 0 and patch >= 0

    @staticmethod
    def from_parts(major: int, minor: int, patch: int) -> SemanticVersion:
        """Create a semantic version from its components."""
        return SemanticVersion(root=f"{major}.{minor}.{patch}")

    @model_validator(mode="after")
    def validate_version(self) -> SemanticVersion:
        """Validate the semantic version string as part of pydantic."""
        if not self.is_valid(self.root):
            raise ValueError(
                f"Invalid semantic version string: got {self.root}, expected <major>.<minor>.<patch>."
                "Each version component must be positive.",
            )
        return self

    @property
    def parts(self) -> SemanticVersionParts:
        """Return the components of the semantic version."""
        major, minor, patch = tuple(map(int, self.root.split(".")))
        return SemanticVersionParts(major, minor, patch)

    def __eq__(self, other: object) -> bool:
        """Check if two semantic versions are equal."""
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self.root == other.root

    def __lt__(self, other: SemanticVersion) -> bool:
        """Compare two semantic versions."""
        return self.parts < other.parts

    def __hash__(self) -> int:
        """Hash the semantic version string."""
        return hash(self.root)

    def __str__(self) -> str:
        """Return the semantic version string."""
        return self.root
