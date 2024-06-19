# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from typing import Any

from cpp_dev.package.cache import PackageCache
from cpp_dev.package.types import PackageRef
from cpp_dev.project.constants import compose_env_dir, compose_env_link_index_dir


class ProjectEnv:
    def __init__(self, project_dir: Path, package_cache: PackageCache) -> None:
        self._env_dir = compose_env_dir(project_dir)
        self._package_cache = package_cache

    def add_package(self, ref: PackageRef) -> None:
        if self._is_package_already_installed(ref):
            print(f"Package {ref} is already installed.")
        transitive_packages_info = self._package_cache.add_package(ref)
        self._link_missing_packages(transitive_packages_info)

    def _is_package_already_installed(self, ref: PackageRef) -> bool:
        return ref in self._get_available_packages()

    def _get_available_packages(self) -> set[PackageRef]:
        index_dir = compose_env_link_index_dir(self._env_dir)
        return [PackageRef(file.name) for file in index_dir.iterdir() if file.is_file()]

    def _link_missing_packages(self, transitive_packages_info: Any) -> None: ...
