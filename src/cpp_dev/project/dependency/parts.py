# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from cpp_dev.common.types import SemanticVersion

###############################################################################
# Public API                                                                ###
###############################################################################


class SemanticVersionWithOptionalParts:
    """A semantic version string with optional parts.

    Valid formats are '<major>', '<major>.<minor>', and '<major>.<minor>.<patch>'.
    """

    def __init__(self, major: int, minor: int | None = None, patch: int | None = None) -> None:
        if minor is None and patch is not None:
            raise ValueError("Cannot specify a patch version without a minor version.")

        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        return (
            f"{self.major}.{self.minor}.{self.patch}"
            if self.patch is not None
            else f"{self.major}.{self.minor}"
            if self.minor is not None
            else str(self.major)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersionWithOptionalParts):
            return NotImplemented
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch


class VersionSpecBoundOperand(Enum):
    """An enumeration of version spec bound operands."""

    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="


@dataclass
class VersionSpecBound:
    """A version spec bound.

    A version spec bound consists of an operand and a semantic version (with potentially optional parts).
    """

    operand: VersionSpecBoundOperand
    version: SemanticVersionWithOptionalParts

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VersionSpecBound):
            return NotImplemented
        return self.operand == other.operand and self.version == other.version


VersionSpecTypeLatest = Literal["latest"]
VersionSpecTypeExact = SemanticVersion
VersionSpecTypeBounds = list[VersionSpecBound]

"""
The version spec type represents either:
o latest
o exact semantic version
o a list of version bounds (representing an AND conjunction)
"""
VersionSpecType = VersionSpecTypeLatest | VersionSpecTypeExact | VersionSpecTypeBounds


@dataclass
class PackageDependencyParts:
    """The result of parsing a package dependency string."""

    repository: str | None
    name: str
    version_spec: VersionSpecType
