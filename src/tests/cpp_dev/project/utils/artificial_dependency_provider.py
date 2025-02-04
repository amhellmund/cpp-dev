# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.provider import Dependency, DependencyIdentifier, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################


class ArtificialDependencyProvider(DependencyProvider):
    """Test implementation of DependencyProvider for testing purposes."""

    def __init__(self, dependencies: list[Dependency]) -> None:
        self._dependencies = {d.id: d for d in dependencies}
        _assert_dependencies_are_complete(self._dependencies)

    def fetch_versions(self, repository: str, name: str) -> list[SemanticVersion]:
        """Fetch available versions for a dependency represented by repository and name."""
        available_versions = [
            dep.id.version
            for dep in self._dependencies.values()
            if dep.id.repository == repository and dep.id.name == name
        ]
        if len(available_versions) == 0:
            raise ValueError(f"No available versions for package {name} at repository {repository}.")
        return sorted(available_versions, reverse=True)

    def collect_dependency_hull(self, _deps: list[DependencySpecifier]) -> set[DependencyIdentifier]:
        """Collect the dependency hull for a list of dependencies."""
        return []

    def install_dependencies(self, _deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
        """Install the dependencies represented by the list of dependency specifiers."""
        return []


###############################################################################
# Implementation                                                            ###
###############################################################################


def _assert_dependencies_are_complete(dependencies: dict[DependencyIdentifier, Dependency]) -> None:
    for dep_id, dependency in dependencies.items():
        for transitive_dep_id in dependency.deps:
            if str(transitive_dep_id) not in dependencies:
                raise ValueError(f"Missing dependency: {transitive_dep_id} for {dep_id}")
