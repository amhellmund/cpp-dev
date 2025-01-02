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
class DependencySpecifierParts:
    """The result of parsing a package dependency string."""

    repository: str | None
    name: str
    version_spec: VersionSpecType
