# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.conan.provider import ConanDependencyProvider
from cpp_dev.dependency.conan.types import ConanPackageReference
from tests.cpp_dev.dependency.conan.utils.env import (ConanTestEnv,
                                                      create_conan_env)
from tests.cpp_dev.dependency.conan.utils.server import (
    ConanServer, launch_conan_test_server)


@dataclass
class ConanTestEnvironment:
    server: ConanServer
    conan: ConanTestEnv


@pytest.fixture
def conan_test_environment(tmp_path: Path, unused_http_port: int) -> Generator[ConanTestEnvironment]:
    with launch_conan_test_server(tmp_path / "server", unused_http_port) as conan_server:
        with create_conan_env(tmp_path / "conan", conan_server.http_port) as conan_env:
            conan_env.create_and_upload_package(ConanPackageReference("cpd/1.0.0@official/cppdev"), [])
            conan_env.create_and_upload_package(ConanPackageReference("cpd/2.0.0@custom/cppdev"), [])
            conan_env.create_and_upload_package(ConanPackageReference("cpd/3.0.0@official/cppdev"), [])
            yield ConanTestEnvironment(
                server=conan_server,
                conan=conan_env
            )


def test_get_available_versions(conan_test_environment: ConanTestEnvironment) -> None:
    provider = ConanDependencyProvider(conan_test_environment.conan.conan_dir)
    assert provider.fetch_versions("official", "cpd") == [
        SemanticVersion("3.0.0"),
        SemanticVersion("1.0.0"),
    ]