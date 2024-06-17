# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from typing import Optional
import httpx

from abc import ABC, abstractmethod
from pathlib import Path


class FileProvider(ABC):
    @abstractmethod
    def get(
        self, path: Path, *, show_progress: bool, message: Optional[str]
    ) -> bytes: ...


class FileProviderLocal(FileProvider):
    def __init__(self, local_store_directory: Path) -> None:
        self._local_store_directory = local_store_directory

    def get(self, path: Path, *, _: bool, message: Optional[str]) -> bytes:
        if message is not None:
            print(message)
        return (self._local_store_directory / path).read_bytes()


class FileProviderRemote(FileProvider):
    def __init__(self, remote_store_url: str) -> None:
        self._remote_store_url = remote_store_url

    def _compose_url(self, *components: Path) -> Path:
        return "/".join(
            [
                self._remote_store_url,
                *components,
            ]
        )

    def get(self, path: Path, *, _: bool, message: Optional[str]) -> bytes:
        if message is not None:
            print(message)
        url = self._compose_url(path)
        response = httpx.get(url)
        return response.content
