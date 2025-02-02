# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from cpp_dev.dependency.conan.command_wrapper import conan_list
from cpp_dev.dependency.conan.setup import CONAN_REMOTE
from cpp_dev.dependency.conan.types import ConanPackageReference
from tests.cpp_dev.dependency.conan.utils.server import \
    launch_conan_test_server

from .env import ConanTestPackage, create_conan_test_env

TEST_PACKAGES = [
    ConanTestPackage(
        ref=ConanPackageReference("dep/1.0.0@official/cppdev"),
        dependencies=[],
        cpp_standard="c++20",
    ),
    ConanTestPackage(
        ref=ConanPackageReference("test/1.0.0@official/cppdev"),
        dependencies=[ConanPackageReference("dep/1.0.0@official/cppdev")],
        cpp_standard="c++20",
    ),
]

def test_create_conan_env(tmp_path: Path, unused_http_port: int) -> None:
    with create_conan_test_env(tmp_path, unused_http_port, TEST_PACKAGES) as conan_env:
        result = conan_list(CONAN_REMOTE, "test")
        assert ConanPackageReference("test/1.0.0@official/cppdev") in result