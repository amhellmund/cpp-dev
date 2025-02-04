# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from cpp_dev.common.types import CppStandard
from cpp_dev.common.utils import create_tmp_dir
from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.conan.command_wrapper import (ConanSettings,
                                                      conan_graph_buildorder,
                                                      conan_list)
from cpp_dev.dependency.conan.setup import CONAN_REMOTE
from cpp_dev.dependency.conan.types import \
    ConanPackageReferenceWithSemanticVersion
from cpp_dev.dependency.conan.utils import conan_env, create_conanfile
from cpp_dev.dependency.provider import Dependency, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier

###############################################################################
# Public API                                                                ###
###############################################################################

class ConanDependencyProvider(DependencyProvider):
    
    def __init__(self, conan_home_dir: Path, profile: str, settings: dict[ConanSetting, object] | None = None) -> None:
        self._conan_home_dir = conan_home_dir
        self._profile = profile
        self._settings = settings

    def fetch_versions(self, repository: str, name: str) -> list[SemanticVersion]:
        with conan_env(self._conan_home_dir):
            package_references = _retrieve_conan_package_references(repository, name)
            available_versions = sorted([ref.version for ref in package_references], reverse=True)
            return available_versions

    def collect_dependency_hull(self, deps: list[DependencySpecifier]) -> list[Dependency]:
        with conan_env(self._conan_home_dir):
            with create_tmp_dir() as tmp_dir:
                conanfile_path = create_conanfile(tmp_dir, deps)
                conan_settings = self._settings if self._settings else {}
                build_order = conan_graph_buildorder(conanfile_path, self._profile, conan_settings)
                _construct_depenencies(build_order.order)
                print(build_order)
                

    def install_dependencies(self, deps: list[DependencySpecifier]) -> list[DependencySpecifier]:
        ... # Implementation using Conan package manager


###############################################################################
# Implementation                                                            ###
###############################################################################

def _retrieve_conan_package_references(repository: str, name: str) -> list[ConanPackageReferenceWithSemanticVersion]:
    package_data = conan_list(CONAN_REMOTE, name)
    package_references = [
        ref
        for ref in package_data.keys()
        if ref.user == repository
    ]
    return package_references

def _construct_depenencies(build_order: list[list[ConanRecipeAttributes]]) -> list[Dependency]:
    ...