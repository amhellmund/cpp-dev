# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from pathlib import Path
from cpp_dev.common.utils import create_tmp_dir, ensure_dir_exists
from cpp_dev.package.store import PackageStore
from cpp_dev.package.types import PackageFileSpecs, PackageIndex, PackageRef
from filelock import FileLock
from shutil import move


@dataclass
class CachedPackage:
    ref: PackageRef
    dependencies: list[PackageRef]
    file_specs: PackageFileSpecs


def _compose_default_cache_dir() -> Path:
    return Path().home() / ".cpp_dev"


def _compose_cache_tmp_dir(cache_dir: Path) -> Path:
    tmp_dir = cache_dir / ".tmp"
    ensure_dir_exists(tmp_dir)
    return tmp_dir


def _compose_cache_index_dir(cache_dir: Path) -> Path:
    return cache_dir / "indexes"


def _compose_cache_packages_dir(cache_dir: Path) -> Path:
    return cache_dir / "packages"


def _compose_cache_lock_file(cache_dir: Path) -> Path:
    return cache_dir / ".lock"


class PackageCache:
    """
    The package cache is responsible for managing the local cache of repository indexes and
    package files retrieved from a store.

    The cache is organized as follows:

      - Repository index files are stored in the 'indexes' directory.
      - Package files are stored in the 'packages' directory.
    """

    def __init__(
        self,
        package_store: PackageStore,
        cache_dir: Path = _compose_default_cache_dir(),
    ) -> None:
        self._package_store = package_store
        self._cache_dir = cache_dir
        self._initialize_cache_if_needed()

    def update_repositories(self) -> None:
        """
        Downloads the index files for all known repositories and stores them locally in the cache.

        This function operates in two steps:

        1. Download the index files to a temporary filesystem location.
        2. Move the downloaded index files under a file-based lock to the target location.
        """
        with create_tmp_dir(self._cache_tmp_dir) as cache_tmp_dir:
            repositories = self._package_store.get_repositories()
            files_to_move = self._write_repository_index_files_to_tmp_dir(
                repositories, cache_tmp_dir
            )
            self._move_index_files_under_lock(files_to_move)

    def add_package(self, package_ref: str) -> list[CachedPackage]: ...

    def _initialize_cache_if_needed(self) -> None:
        if not self._cache_dir.exists():
            self._cache_tmp_dir = ensure_dir_exists(
                _compose_cache_tmp_dir(self._cache_dir)
            )
            self._cache_indexes_dir = ensure_dir_exists(
                _compose_cache_index_dir(self._cache_dir)
            )
            self._cache_packages_dir = ensure_dir_exists(
                _compose_cache_packages_dir(self._cache_dir)
            )

    def _write_repository_index_files_to_tmp_dir(
        self,
        repositories: list[str],
        cache_tmp_dir: Path,
    ) -> list[Path]:
        files_to_move_under_lock: list[Path] = []
        for repository in repositories:
            index_content = self._package_store.get_index(repository)
            index = _validate_package_index(index_content, repository)

            index_path = cache_tmp_dir / f"{repository}.json"
            index_path.write_text(index.model_dump_json())

            files_to_move_under_lock.append(index_path)

        return files_to_move_under_lock

    def _move_index_files_under_lock(self, files: list[Path]) -> None:
        cache_indexes_dir = self._cache_indexes_dir
        cache_lock_file = _compose_cache_lock_file(self._cache_dir)
        lock = FileLock(cache_lock_file)
        with lock:
            for file in files:
                move(file, cache_indexes_dir / file.name)

    def get_transitive_dependencies(self, package_ref: str) -> list[PackageRef]: ...


def _validate_package_index(content: bytes, requested_repository: str) -> PackageIndex:
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
