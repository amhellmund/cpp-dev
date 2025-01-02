# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from cpp_dev.common.types import SemanticVersion
from cpp_dev.dependency.specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################

CppStandard = Literal["c++11", "c++14", "c++17", "c++20", "c++23"]


@dataclass
class Dependency:
    """A software package containing libraries, headers and executables."""

    specifier: DependencySpecifier
    cpp_standard: CppStandard
    deps: list[Dependency]


class DependencyProvider(ABC):
    """Abstract base class for dependency providers.

    A dependency provider is responsible for resolving, downloading and installing dependencies.
    A dependency is a software package containing libraries, headers and executables.
    Each dependency is identified by a dependency string
    """

    @abstractmethod
    def fetch_versions(self, repository: str, name: str) -> list[SemanticVersion]:
        """Fetch available versions for a dependency represented by repository and name.

        Args:
            repository (str): The repository of the dependency.
            name (str): The name of the dependency.

        Result:
            The list of available versions sorted in reverse order such that the latest version is first.

        """

    @abstractmethod
    def collect_dependency_hull(self, deps: list[DependencySpecifier]) -> dict[str, str]:
        """Collect the dependency hull for a list of dependencies."""
