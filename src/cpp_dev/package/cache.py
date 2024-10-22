# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from cpp_dev.common.utils import create_tmp_dir, ensure_dir_exists
from cpp_dev.package.store import PackageStore
from cpp_dev.package.types import PackageFileSpecs, PackageIndex, PackageRef
from filelock import FileLock, Timeout
from shutil import move
from zipfile import ZipFile


@dataclass
class CachedPackage:
    ref: PackageRef
    file_specs: PackageFileSpecs


def _compose_default_cache_dir() -> Path:
    return Path().home() / ".cpp_dev"


def _compose_cache_tmp_dir(cache_dir: Path) -> Path:
    tmp_dir = cache_dir / ".tmp"
    return tmp_dir


def _compose_cache_index_dir(cache_dir: Path) -> Path:
    return cache_dir / "indexes"


def _compose_cache_packages_dir(cache_dir: Path) -> Path:
    return cache_dir / "packages"


def _compose_cache_lock_file(
    cache_dir: Path, timeout: Optional[float] = None
) -> FileLock:
    return FileLock(cache_dir / ".lock", timeout=timeout)


def _write_package_completion_file(package_path: Path) -> None:
    completion_file = package_path.with_suffix(".complete")
    completion_file.touch()


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
        self._cache_tmp_dir = _compose_cache_tmp_dir(self._cache_dir)
        self._cache_indexes_dir = _compose_cache_index_dir(self._cache_dir)
        self._cache_packages_dir = _compose_cache_packages_dir(self._cache_dir)
        self._initialize_cache_if_needed()

    def _initialize_cache_if_needed(self) -> None:
        print(self._cache_dir)
        if not self._cache_dir.exists():
            ensure_dir_exists(self._cache_dir)
            ensure_dir_exists(self._cache_tmp_dir)
            ensure_dir_exists(self._cache_indexes_dir)
            ensure_dir_exists(self._cache_packages_dir)

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

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
                repositories,
                cache_tmp_dir,
            )
            self._move_index_files_under_lock(files_to_move)

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
        cache_lock = _compose_cache_lock_file(self._cache_dir)
        try:
            with cache_lock:
                for file in files:
                    print(file)
                    move(file, self._cache_indexes_dir / file.name)
        except Timeout:
            raise RuntimeError("The cache is already in use by another process.")

    def get_package_with_dependencies(self, ref: PackageRef) -> list[CachedPackage]:
        """
        Retrieves the package with the given package reference and its transitive dependencies.

        If the package(s) are not already cached, they will be downloaded from the package store.

        The function returns a list of cached packages that include specifications on how-to use the
        packages (e.g. libraries, include files).
        The order of the list is unspecified with regard to the topological order of the dependencies.
        """
        packages = self._resolve_package_with_dependencies(ref)
        cached_packages = set()
        for package in packages:
            cached_package = self._get_cached_package(package)
            if cached_package is None:
                self._download_and_cache_package(package)
                cached_package = self._get_cached_package(package)
            cached_packages.add(cached_package)

        return cached_packages

    def _resolve_package_with_dependencies(self, ref: PackageRef) -> set[PackageRef]:
        """
        Resolves a package reference to a list of package references considering the transitive dependencies.
        """
        resolved_packages = set()
        packages_to_resolve = [ref]
        while len(packages_to_resolve) > 0:
            next_ref = packages_to_resolve.pop()
            resolved_packages.add(next_ref)

            repository, package, version = next_ref.unpack
            index = self._get_repository_index(repository)

            if package not in index.packages:
                raise ValueError(
                    f"Package {package} not found in repository {repository}. Consider updating the repository indices."
                )
            if version not in index.packages[package].versions:
                raise ValueError(
                    f"Version {version} not found for package {package} in repository {repository}. Consider updating the repository indices."
                )

        return resolved_packages

    def _get_repository_index(self, repository: str) -> PackageIndex:
        index_path = self._cache_indexes_dir / f"{repository}.json"
        if not index_path.exists():
            raise ValueError(
                f"Repository index for {repository} not found in cache. Consider updating the repository indices."
            )
        return _validate_package_index(index_path.read_text(), repository)

    def _get_cached_package(self, ref: PackageRef) -> Optional[CachedPackage]:
        package_path = self._cache_packages_dir / ref
        if not package_path.exists():
            self._download_and_cache_package(ref)
        return self._load_cached_package(ref)

    def _download_and_cache_package(self, ref: PackageRef) -> CachedPackage:
        with create_tmp_dir(self._cache_tmp_dir) as cache_tmp_dir:
            package_tmp_file = cache_tmp_dir / f"{ref}.zip"
            package_tmp_file.write_bytes(self._package_store.get_package_file(ref))

            extract_dir = cache_tmp_dir / ref
            with ZipFile(package_tmp_file, "r") as zip_file:
                zip_file.extractall(extract_dir)

            self._move_package_file_under_lock(extract_dir)
            return self._load_cached_package(ref)

    def _move_package_file_under_lock(self, package_path: Path) -> None:
        cache_lock = _compose_cache_lock_file(self._cache_dir)
        try:
            with cache_lock:
                move(package_path, self._cache_packages_dir)
        except Timeout:
            raise RuntimeError("The cache is already in use by another process.")

    def _load_cached_package(self, ref: PackageRef) -> CachedPackage: ...


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
