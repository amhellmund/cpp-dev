# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import subprocess
import time
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

import requests

from cpp_dev.common.utils import ensure_dir_exists
from cpp_dev.dependency.conan.setup import (DEFAULT_CONAN_USER,
                                            DEFAULT_CONAN_USER_PWD)

###############################################################################
# Public API                                                                ###
###############################################################################

@dataclass
class ConanServer:
    hostname: str
    http_port: int
    user: str
    password: str

    def compose_url(self) -> str:
        return f"http://{self.hostname}:{self.http_port}"

@contextmanager
def launch_conan_server(server_dir: Path, http_port: int) -> Generator[ConanServer]:
    """Launch a Conan server."""
    connection_params = _create_conan_server_config(server_dir, http_port)
    process = _launch_conan_server(server_dir)
    _wait_for_server_start(connection_params)
    try:
        yield connection_params
    finally:
        _stop_process(process)


###############################################################################
# Implementation                                                            ###
###############################################################################

_CONAN_SERVER_CONFIG = dedent("""
    [server]
    jwt_secret: IJKhyoioUINMXCRTytrR
    jwt_expire_minutes: 120

    ssl_enabled: False
    port: {http_port}

    host_name: localhost

    disk_storage_path: {disk_storage_path}

    [write_permissions]
    */*@*/*: {default_user}

    [read_permissions]
    */*@*/*: {default_user}

    [users]
    {default_user}: {default_password}
""")

def _create_conan_server_config(server_dir: Path, http_port: int) -> ConanServer:
    ensure_dir_exists(server_dir)
    server_config = server_dir / "server.conf"
    server_storage_path = server_dir / "data"
    server_config.write_text(_CONAN_SERVER_CONFIG.format(
        http_port=http_port,
        disk_storage_path=server_storage_path,
        default_user=DEFAULT_CONAN_USER,
        default_password=DEFAULT_CONAN_USER_PWD,
    ))
    return ConanServer(
        hostname="localhost",
        http_port=http_port,
        user=DEFAULT_CONAN_USER,
        password=DEFAULT_CONAN_USER_PWD
    )

def _launch_conan_server(server_dir: Path) -> subprocess.Popen:
    process = subprocess.Popen(
        args=[
            "conan_server",
            "--server_dir",
            str(server_dir)
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    return process  # Read the server output to ensure it"s started

def _wait_for_server_start(conan_server: ConanServer) -> None:
    for _ in range(10):
        try:
            response = requests.get(f"{conan_server.compose_url()}/v1/ping")
            response.raise_for_status()
            return
        except requests.exceptions.RequestException:
            time.sleep(0.1)
    raise RuntimeError("Failed to start Conan server")

def _stop_process(process: subprocess.Popen) -> None:
    process.terminate()