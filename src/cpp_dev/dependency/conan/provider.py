# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from cpp_dev.common.types import CppStandard
from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.conan.utils import conan_env
from cpp_dev.dependency.provider import Dependency, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################

class ConanDependencyProvider(DependencyProvider):
    
    def __init__(self, conan_home_dir: Path) -> None:
        self._conan_home_dir = conan_home_dir

    def fetch_versions(self, repository: str, name: str) -> list[SemanticVersion]:
        with conan_env()

    def collect_dependency_hull(self, deps: list[DependencySpecifier]) -> list[Dependency]:
        ... # Implementation using Conan package manager

    def install_dependencies(self, deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
        ... # Implementation using Conan package manager