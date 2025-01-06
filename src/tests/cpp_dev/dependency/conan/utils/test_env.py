# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from cpp_dev.conan.command_wrapper import conan_list
from cpp_dev.conan.setup import CONAN_REMOTE
from cpp_dev.conan.types import ConanPackageReference

from .env import create_conan_env
from .server import launch_conan_server


def test_create_conan_env(tmp_path: Path, unused_http_port: int) -> None:
    with launch_conan_server(tmp_path / "server", unused_http_port) as conan_server:
        with create_conan_env(tmp_path / "conan", conan_server.http_port) as conan_env:
            conan_env.create_and_upload_package(ConanPackageReference("dep/1.0.0@official/cppdev"), [])
            conan_env.create_and_upload_package(ConanPackageReference("test/1.0.0@official/cppdev"), [ConanPackageReference("dep/1.0.0@official/cppdev")])
            result = conan_list(CONAN_REMOTE, "test")
            assert "test/1.0.0@official/cppdev" in result