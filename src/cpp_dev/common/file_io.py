# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from typing import Callable, Optional
import httpx

from abc import ABC, abstractmethod
from pathlib import Path


type StrOrPath = str | Path
type ProgressCallback = Callable[[ProgressNotification], None]


@dataclass
class ProgressNotification:
    total_size_bytes: int
    retrieved_bytes: int


def _trigger_progess_complete(
    content: bytes,
    callback: Optional[ProgressCallback],
) -> None:
    if callback:
        callback(
            ProgressNotification(
                total_size_bytes=len(content),
                retrieved_bytes=len(content),
            )
        )


class FileIO(ABC):
    """
    Interface to read files from from an implementation-defined source.
    """

    @abstractmethod
    def get(
        self,
        path: StrOrPath,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> bytes: ...


class FileIOLocal(FileIO):
    """
    Implementation of FileIO that reads files from the local file system.
    """

    def __init__(self, local_store_directory: Path) -> None:
        self._local_store_directory = local_store_directory

    def get(
        self,
        path: StrOrPath,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> bytes:
        content = (self._local_store_directory / path).read_bytes()
        _trigger_progess_complete(content, progress_callback)
        return content


class FileIORemote(FileIO):
    """
    Implementation of FileIO that reads files from a remote server via HTTP.
    """

    def __init__(self, remote_store_url: str) -> None:
        self._remote_store_url = remote_store_url

    def _compose_url(self, *components: StrOrPath) -> Path:
        return "/".join(
            [
                self._remote_store_url,
                *components,
            ]
        )

    def get(
        self,
        path: StrOrPath,
        progress_callback: Optional[ProgressCallback] = None,
    ) -> bytes:
        url = self._compose_url(path)
        response = httpx.get(url)
        _trigger_progess_complete(response.content, progress_callback)
        return response.content
