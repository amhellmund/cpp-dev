# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from cpp_dev.common._types import CppStandard, SemanticVersion


class PackageDependency(BaseModel):
    name: str
    repository: str
    version: SemanticVersion


class ProjectConfig(BaseModel):
    name: str
    version: SemanticVersion
    std: CppStandard

    author: Optional[str]
    license: Optional[str]
    description: Optional[str]

    dependencies: list[PackageDependency]
    dev_dependencies: list[PackageDependency]
