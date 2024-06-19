# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from cpp_dev.package.store import PackageStore
from cpp_dev.package.types import PackageFileSpecs, PackageIndex, PackageRef


@dataclass
class CachedPackage:
    ref: PackageRef
    dependencies: list[PackageRef]
    file_specs: PackageFileSpecs


class PackageCache:
    def __init__(self, package_store: PackageStore) -> None:
        self._package_store = package_store

    def update_repositories(self) -> None:
        repositories = self._package_store.get_repositories()
        for repository in repositories:
            index_content = self._package_store.get_index(repository)
            index = _validate_package_index(index_content, repository)

    def get_transitive_dependencies(self, package_ref: str) -> list[PackageRef]: ...

    def add_package(self, package_ref: str) -> list[CachedPackage]: ...


def _validate_package_index(content: bytes, requested_repository: str) -> PaackageIndex:
    index = PackageIndex.model_validate_json(content)
    if index.repository != requested_repository:
        raise ValueError(
            f"Package index inconsistency detected: got {index.repository}, expected {requested_repository}"
        )
    for name, specs in index.packages.items():
        if not specs.versions:
            raise ValueError(
                f"Package index inconsistency detected: package {name} has no versions"
            )
    return index
