# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cpp_dev.dependency.conan.command_wrapper import (conan_create,
                                                      conan_graph_buildorder,
                                                      conan_list,
                                                      conan_remote_login,
                                                      conan_upload)
from cpp_dev.dependency.conan.setup import CONAN_REMOTE
from cpp_dev.dependency.conan.types import ConanPackageReference
from cpp_dev.dependency.conan.utils import conan_env

from .utils.env import ConanTestEnv, create_conan_env
from .utils.server import ConanServer, launch_conan_server

MockType = MagicMock | AsyncMock

@pytest.fixture
def patched_run_command_assert_success() -> Generator[MockType]:
    with patch("cpp_dev.dependency.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        yield mock_run_command

def test_conan_remote_login(patched_run_command_assert_success: MockType) -> None:
    conan_remote_login(CONAN_REMOTE, "user", "password")
    patched_run_command_assert_success.assert_called_once_with(
        "conan",
        "remote",
        "login",
        CONAN_REMOTE,
        "user",
        "-p",
        "password",
    )

def test_conan_create(patched_run_command_assert_success: MockType) -> None:
    conan_create(Path("package_dir"), "profile")
    patched_run_command_assert_success.assert_called_once_with(
        "conan",
        "create",
        "package_dir",
        "-pr:a", "profile",
    )

def test_conan_upload(patched_run_command_assert_success: MockType) -> None:
    package_ref = ConanPackageReference("cpd/1.0.0@official/cppdev")
    conan_upload(package_ref, CONAN_REMOTE)
    patched_run_command_assert_success.assert_called_once_with(
        "conan",
        "upload",
        "-r", CONAN_REMOTE,
        str(package_ref),
    )

@dataclass
class ConanTestEnvironment:
    server: ConanServer
    conan: ConanTestEnv

@pytest.fixture
def conan_test_environment(tmp_path: Path, unused_http_port: int) -> Generator[ConanTestEnvironment]:
    with launch_conan_server(tmp_path / "server", unused_http_port) as server:
        with create_conan_env(tmp_path / "conan", server.http_port) as conan:
            conan.create_and_upload_package(ConanPackageReference("dep/1.0.0@official/cppdev"), [])
            conan.create_and_upload_package(ConanPackageReference("cpd1/1.0.0@official/cppdev"), [])
            conan.create_and_upload_package(ConanPackageReference("cpd/1.0.0@official/cppdev"), [ConanPackageReference("dep/1.0.0@official/cppdev")])
            yield ConanTestEnvironment(
                server=server,
                conan=conan,
            )


@pytest.mark.usefixtures("conan_test_environment")
def test_conan_list() -> None:
    result = conan_list(CONAN_REMOTE, "cpd")
    assert len(result) == 1
    assert ConanPackageReference("cpd/1.0.0@official/cppdev") in result


@pytest.mark.usefixtures("conan_test_environment")
def test_conan_graph_buildorder(tmp_path: Path, conan_test_environment: ConanTestEnvironment) -> None:
    conanfile_path = tmp_path / "conanfile.txt"
    conanfile_path.write_text(dedent("""
        [requires]
        cpd/1.0.0@official/cppdev
        """)
    )
    graph_build_order = conan_graph_buildorder(conanfile_path, conan_test_environment.conan.profile)
    assert len(graph_build_order.order) == 2
    assert len(graph_build_order.order[0]) == 1
    dep_recipe = graph_build_order.order[0][0]
    assert dep_recipe.ref.startswith("dep/1.0.0@official/cppdev")

    assert len(graph_build_order.order[1]) == 1
    cpd_recipe = graph_build_order.order[1][0]
    assert cpd_recipe.ref.startswith("cpd/1.0.0@official/cppdev")
    assert len(cpd_recipe.depends) == 1
    assert cpd_recipe.depends[0].startswith("dep/1.0.0@official/cppdev")
        

