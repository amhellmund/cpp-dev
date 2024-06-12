# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from abc import ABC, abstractmethod
from pathlib import Path

from cpp_dev.package.types import PackageRef


class PackageResolver(ABC):
    @abstractmethod
    def provide_package_with_transitive_dependencies(
        self,
        package_ref: PackageRef,
        target_dir: Path,
    ) -> list[Path]:
        """
        This function transitively resolves the package reference and makes available the package and its dependency
        in the target directory.
        """
        ...


class PackageResolverLocal(ABC):
    def __init__(self, local_store_directory: Path) -> None:
        self.local_store_directory = local_store_directory

    def provide_package_with_transitive_dependencies(
        self,
        package_ref: PackageRef,
        target_dir: Path,
    ) -> list[Path]: ...


class PackageResolverRemote(ABC):
    def __init__(self, remote_store_url: str) -> None:
        self.remote_store_url = remote_store_url

    def provide_package_with_transitive_dependencies(
        self,
        package_ref: PackageRef,
        target_dir: Path,
    ) -> list[Path]: ...
