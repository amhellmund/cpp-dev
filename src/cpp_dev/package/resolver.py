# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.common.types import PackageRef
from cpp_dev.package.types import PackageIndex
from .artifact_downloader import ArtifactDownloader


class PackageResolver:
    def __init__(self, artifact_downloader: ArtifactDownloader):
        self._artifact_downloader = artifact_downloader
        self._repository_index_cache: dict[str, PackageIndex] = dict()

    def _get_repository_index(self, repository: str) -> PackageIndex:
        """
        Gets the package index for the given repository.
        """
        if repository not in self._repository_index_cache:
            index = self._artifact_downloader.get_index(repository)
            self._repository_index_cache[repository] = index
        return self._repository_index_cache[repository]

    def resolve(self, ref: PackageRef) -> set[PackageRef]:
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

        return resolved_packages
