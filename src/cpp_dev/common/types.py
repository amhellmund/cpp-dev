# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CppStandard = Literal["11", "14", "17", "20", "23"]


@dataclass
class SemanticVersion:
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_string(version: str) -> SemanticVersion:
        components = version.split(".")
        if len(components) != 3:
            raise ValueError(f"Invalid semantic version: got {version}, expected <major>.<minor>.<patch>")
        
        major, minor, patch = map(int, components)
        return SemanticVersion(major, minor, patch)