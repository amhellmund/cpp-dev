# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pydantic import BaseModel

from cpp_dev.common.types import CppStandard, SemanticVersion
from cpp_dev.dependency.types import PackageDependency

###############################################################################
# Public API                                                                ###
###############################################################################


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
