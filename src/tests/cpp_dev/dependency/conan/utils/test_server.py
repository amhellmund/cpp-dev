# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

import requests

from .server import launch_conan_server


def test_launch_conan_server(tmp_path: Path, unused_http_port: int) -> None:
    with launch_conan_server(tmp_path / "server", unused_http_port) as conan_server:
        response = requests.get(conan_server.compose_url() + "/v1/ping", timeout=2)
        assert response.status_code == 200