# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pydantic import BaseModel

from cpp_dev.common.types import CppStandard, SemanticVersion


class PackageDependency(BaseModel):
    """A package dependency for a project."""

    name: str
    repository: str
    version: SemanticVersion


class ProjectConfig(BaseModel):
    """A project configuration for a cpp-dev project."""

    name: str
    version: SemanticVersion
    std: CppStandard

    author: str | None
    license: str | None
    description: str | None

    dependencies: list[PackageDependency]
    dev_dependencies: list[PackageDependency]
