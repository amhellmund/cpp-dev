# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel, RootModel, model_validator, ValidationError

from cpp_dev.common.types import CppStandard

class SemanticVersion(RootModel):
    root: str
    
    @model_validator(mode="after")
    def validate_version(self) -> SemanticVersion:
        components = self.root.split(".")
        if len(components) != 3:
            raise ValidationError(f"Invalid semantic version string: got {self.root}, expected <major>.<minor>.<patch>")
        
        major, minor, patch = map(int, components)
        if major < 0 or minor < 0 or patch < 0:
            raise ValidationError(f"Invalid semantic version string: got {self.root}, expected positive integers")

        return self


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


