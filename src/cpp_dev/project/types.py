# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from typing import Literal

from pydantic import BaseModel

from cpp_dev.common.types import CppStandard, SemanticVersion

from .dependency.types import PackageDependency

###############################################################################
# Public API                                                                ###
###############################################################################

DependencyType = Literal["runtime", "dev", "cpd"]


class ProjectConfig(BaseModel):
    """A project configuration for a cpp-dev project."""

    name: str
    version: SemanticVersion
    std: CppStandard

    author: str | None
    license: str | None
    description: str | None

    # Public dependencies used by the project
    dependencies: list[PackageDependency]

    # Development dependencies used by the project while developing
    dev_dependencies: list[PackageDependency]

    # Cpp-Dev dependencies used by the tool itself. These dependencies can only be updated but not removed.
    cpd_dependencies: list[PackageDependency]

    def get_dependencies(self, dep_type: DependencyType) -> list[PackageDependency]:
        """Return the dependency list by type."""
        if dep_type == "runtime":
            return self.dependencies
        if dep_type == "dev":
            return self.dev_dependencies
        if dep_type == "cpd":
            return self.cpd_dependencies
        raise ValueError(f"Invalid dependency type requested: {dep_type}")
        raise ValueError(f"Invalid dependency type requested: {dep_type}")
