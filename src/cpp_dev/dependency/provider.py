# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from cpp_dev.common.types import CppStandard
from cpp_dev.common.version import SemanticVersion

from .specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################


class DependencyError(Exception):
    """Exception for raising issues during dependency resolution or installation."""


@dataclass
class Dependency:
    """A software package containing libraries, headers and executables."""

    specifier: DependencySpecifier
    cpp_standard: CppStandard
    deps: list[DependencySpecifier]


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
    def collect_dependency_hull(self, deps: list[DependencySpecifier]) -> list[Dependency]:
        """Collect the dependency hull for a list of dependencies.

        Args:
            deps (list[DependencySpecifier]): The list of dependencies to collect the dependency hull for.

        Return:
            The list of dependencies that form the dependency hull (i.e. including transitive dependencies)
            for the input list of dependencies.

        Raise:
            DependencyError: If an error occurs during dependency resolution.

        """

    @abstractmethod
    def install_dependencies(self, deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
        """Install the dependencies represented by the input list.

        Args:
            deps (list[DependencySpecifier]): The list of dependencies to install.

        Return:
            The list of successfully installed dependencies (including transitive dependencies).

        Raise:
            DependencyError: If an error occurs during dependency rinstallation.

        """
