# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel, model_serializer, model_validator

from cpp_dev.common.types import CppStandard

class SemanticVersion(BaseModel):
    major: int
    minor: int
    patch: int

    @staticmethod
    def from_string(version: str) -> SemanticVersion:
        components = version.split(".")
        if len(components) != 3:
            raise ValueError(f"Invalid semantic version string: got {version}, expected <major>.<minor>.<patch>")
        
        major, minor, patch = map(int, components)
        return SemanticVersion(major=major, minor=minor, patch=patch)


class PackageDependency(BaseModel):
    name: str
    repository: str
    version: SemanticVersion


class PackageConfig(BaseModel):
    format_version: int
    
    name: str
    version: SemanticVersion
    std: CppStandard
    
    author: Optional[str]
    license: Optional[str]
    description: Optional[str]

    dependencies: list[PackageDependency]
