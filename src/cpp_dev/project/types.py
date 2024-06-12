# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from cpp_dev.common.types import CppStandard, SemanticVersion


class PackageDependency(BaseModel):
    name: str
    repository: str
    version: SemanticVersion


class ProjectConfig(BaseModel):
    format_version: int

    name: str
    version: SemanticVersion
    std: CppStandard

    author: Optional[str]
    license: Optional[str]
    description: Optional[str]

    dependencies: list[PackageDependency]
    dev_dependencies: list[PackageDependency]
