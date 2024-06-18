# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from cpp_dev.common.file_io import FileIO, ProgressNotification

from cpp_dev.package.constants import compose_index_path, compose_package_path

from .types import OperatingSystem, PackageRef


class ArtifactIO:
    def __init__(self, file_io: FileIO, os: OperatingSystem) -> None:
        self._file_io = file_io
        self._os = os

    def get_index(self, repository: str) -> bytes:
        index_path = compose_index_path(self._os, repository)
        return self._file_io.get(index_path, progress_callback=None)

    def get_package_file(self, ref: PackageRef) -> bytes:
        def _progress_callback(progress: ProgressNotification) -> None:
            print(
                f"Downloading {ref}: {progress.retrieved_bytes} / {progress.total_size_bytes} bytes"
            )

        package_path = compose_package_path(self._os, ref)
        return self._file_io.get(package_path, progress_callback=_progress_callback)


# def _validate_package_index(index: PackageIndex, requested_repository: str) -> None:
#     if index.repository != requested_repository:
#         raise ValueError(
#             f"Package index inconsistency detected: got {index.repository}, expected {requested_repository}"
#         )
#     for name, specs in index.packages.items():
#         if not specs.versions:
#             raise ValueError(
#                 f"Package index inconsistency detected: package {name} has no versions"
#             )
