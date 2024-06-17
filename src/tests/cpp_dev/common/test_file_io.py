# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path
import pytest
from pytest_httpserver import HTTPServer

from cpp_dev.common.file_io import FileIOLocal, FileIORemote


@pytest.fixture()
def test_data_path() -> Path:
    return Path(__file__).parent / "data"


def test_file_io_local(test_data_path: Path):
    resolver = FileIOLocal(test_data_path)
    assert resolver.get("file.txt", progress_callback=None) == b"content"


@pytest.fixture
def http_file_server(httpserver: HTTPServer, test_data_path: Path) -> HTTPServer:
    files = [file for file in test_data_path.glob("**/*") if file.is_file()]
    for file in files:
        rel_path = file.relative_to(test_data_path)
        httpserver.expect_request(f"/{rel_path}").respond_with_data(file.read_bytes())
    return httpserver


def test_file_io_remote(http_file_server: HTTPServer):
    resolver = FileIORemote(
        http_file_server.url_for("/"),
    )
    assert resolver.get("file.txt", progress_callback=None) == b"content"
