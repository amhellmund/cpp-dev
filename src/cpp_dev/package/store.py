# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
from cpp_dev.common.file_io import FileIO, ProgressNotification
from pydantic import TypeAdapter

from .types import OperatingSystem, PackageRef


class PackageStore:
    def __init__(self, file_io: FileIO, os: OperatingSystem) -> None:
        self._file_io = file_io
        self._os = os

    def get_repositories(self) -> list[str]:
        repositories_path = compose_repositories_path(self._os)
        repositories_raw = self._file_io.get(repositories_path, progress_callback=None)
        return TypeAdapter(list[str]).validate_json(repositories_raw)

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


def compose_index_path(os: OperatingSystem, repository: str) -> Path:
    return Path("indexes") / os.compose_canonical_path() / f"{repository}.json"


def compose_package_path(os: OperatingSystem, ref: PackageRef) -> Path:
    repository, name, version = ref.unpack
    print(repository, name, version)
    return (
        Path("packages")
        / os.compose_canonical_path()
        / f"{repository}"
        / f"{name}-{version}.zip"
    )


def compose_repositories_path(os: OperatingSystem) -> Path:
    return Path("repositories") / os.compose_canonical_path() / "repositories.json"
