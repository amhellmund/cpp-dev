# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

import httpx

from abc import ABC, abstractmethod
from pathlib import Path

from cpp_dev.common.types import OperatingSystemDistribution

from .types import PackageIndex


class PackageResolver(ABC):
    @abstractmethod
    def get_index(
        self,
        repository: str,
    ) -> PackageIndex: ...

    @abstractmethod
    def get_package_file(
        self,
        path: Path,
    ) -> bytes: ...


class PackageResolverLocal(ABC):
    def __init__(
        self, local_store_directory: Path, distro: OperatingSystemDistribution
    ) -> None:
        self._local_store_directory = local_store_directory
        self._distro = distro

    def _compose_path(self, *components: Path) -> Path:
        return (
            self._local_store_directory / self._distro.name / self._distro.version
        ).joinpath(*components)

    def get_index(self, repository: str) -> PackageIndex:
        index_file = self._compose_path("index", f"{repository}.json")
        index = PackageIndex.model_validate_json(index_file.read_text())
        _validate_package_index(index, repository)
        return index

    def get_package_file(self, path: Path) -> bytes:
        package_file = self._compose_path("packages", path)
        return package_file.read_bytes()


class PackageResolverRemote(ABC):
    def __init__(
        self, remote_store_url: str, distro: OperatingSystemDistribution
    ) -> None:
        self._remote_store_url = remote_store_url
        self._distro = distro

    def _compose_url(self, *components: Path) -> Path:
        return "/".join(
            [
                self._remote_store_url,
                self._distro.name,
                self._distro.version,
                *components,
            ]
        )

    def get_index(self, repository: str) -> PackageIndex:
        index_url = self._compose_url("index", f"{repository}.json")
        response = httpx.get(index_url)
        index = PackageIndex.model_validate_json(response.text)
        _validate_package_index(index, repository)
        return index

    def get_package_file(self, path: Path) -> bytes:
        package_url = self._compose_url("packages", f"{path}")
        response = httpx.get(package_url)
        return response.content


def _validate_package_index(index: PackageIndex, requested_repository: str) -> None:
    if index.repository != requested_repository:
        raise ValueError(
            f"Package index inconsistency detected: got {index.repository}, expected {requested_repository}"
        )
    for package in index.packages:
        if not package.versions:
            raise ValueError(
                f"Package inconsistency detected: package {package.name} has no versions"
            )
        if package.latest not in package.versions:
            raise ValueError(
                f"Package inconsistency detected: package {package.name} has no latest version"
            )
