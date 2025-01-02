# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from cpp_dev.common.types import CppStandard
from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.provider import Dependency, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################

class ConanDependencyProvider(DependencyProvider):
    
    def __init__(self) -> None:
        ...

    def fetch_versions(self, repository: str, name: str) -> list[SemanticVersion]:
        ... # Implementation using Conan package manager

    def collect_dependency_hull(self, deps: list[DependencySpecifier]) -> list[Dependency]:
        ... # Implementation using Conan package manager

    def install_dependencies(self, deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
        ... # Implementation using Conan package manager