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
                                                      ConanTestPackage,
                                                      create_conan_test_env)
from tests.cpp_dev.dependency.conan.utils.server import (
    ConanServer, launch_conan_test_server)


@pytest.fixture
def conan_test_environment(tmp_path: Path, unused_http_port: int) -> Generator[ConanTestEnv]:
    TEST_PACKAGES = [
        ConanTestPackage(
            ref=ConanPackageReference("cpd/1.0.0@official/cppdev"),
            dependencies=[],
            cpp_standard="c++17",
        ),
        ConanTestPackage(
            ref=ConanPackageReference("cpd/2.0.0@custom/cppdev"),
            dependencies=[],
            cpp_standard="c++17",
        ),
        ConanTestPackage(
            ref=ConanPackageReference("cpd/3.0.0@official/cppdev"),
            dependencies=[],
            cpp_standard="c++17",
        ),
    ]
    with create_conan_test_env(tmp_path, unused_http_port, TEST_PACKAGES) as conan_test_env:
        yield conan_test_env


def test_get_available_versions(conan_test_environment: ConanTestEnv) -> None:
    provider = ConanDependencyProvider(conan_test_environment.conan_home_dir)
    assert provider.fetch_versions("official", "cpd") == [
        SemanticVersion("3.0.0"),
        SemanticVersion("1.0.0"),
    ]