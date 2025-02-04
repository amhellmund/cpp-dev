# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from pathlib import Path
from textwrap import dedent
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cpp_dev.dependency.conan.command_wrapper import (ConanCommandException,
                                                      ConanSettings,
                                                      conan_create,
                                                      conan_graph_buildorder,
                                                      conan_list,
                                                      conan_remote_login,
                                                      conan_upload)
from cpp_dev.dependency.conan.setup import CONAN_REMOTE
from cpp_dev.dependency.conan.types import \
    ConanPackageReferenceWithSemanticVersion

from .utils.env import ConanTestEnv, ConanTestPackage, create_conan_test_env
from .utils.server import launch_conan_test_server

MockType = MagicMock | AsyncMock

@pytest.fixture
def patched_run_command_assert_success() -> Generator[MockType]:
    with patch("cpp_dev.dependency.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        yield mock_run_command

def test_conan_create(patched_run_command_assert_success: MockType) -> None:
    # todo: this test currently uses a mock, but wil later be changed to test with a real server.
    conan_create(Path("package_dir"), "profile", {"compiler": "test", "compiler.cppstd": "c++20"})
    patched_run_command_assert_success.assert_called_once_with(
        "conan",
        "create",
        "package_dir",
        "-pr:a", "profile",
        "-s:a", "compiler=test",
        "-s:a", "compiler.cppstd=c++20",
    )

def test_conan_upload(patched_run_command_assert_success: MockType) -> None:
    # todo: this test currently uses a mock, but wil later be changed to test with a real server.
    package_ref = ConanPackageReferenceWithSemanticVersion("cpd/1.0.0@official/cppdev")
    conan_upload(package_ref, CONAN_REMOTE)
    patched_run_command_assert_success.assert_called_once_with(
        "conan",
        "upload",
        "-r", CONAN_REMOTE,
        str(package_ref),
    )


@pytest.fixture
def conan_test_environment(tmp_path: Path, unused_http_port: int) -> Generator[ConanTestEnv]:
    with launch_conan_test_server(tmp_path, unused_http_port) as server:
        TEST_PACKAGES = [
            ConanTestPackage(
                ref=ConanPackageReferenceWithSemanticVersion("dep/1.0.0@official/cppdev"),
                dependencies=[],
                cpp_standard="c++20",
            ),
            ConanTestPackage(
                ref=ConanPackageReferenceWithSemanticVersion("dep/2.0.0@official/cppdev"),
                dependencies=[],
                cpp_standard="c++20",
            ),
            ConanTestPackage(
                ref=ConanPackageReferenceWithSemanticVersion("cpd/1.0.0@official/cppdev"),
                dependencies=[ConanPackageReferenceWithSemanticVersion("dep/1.0.0@official/cppdev")],
                cpp_standard="c++20",
            ),
            ConanTestPackage(
                ref=ConanPackageReferenceWithSemanticVersion("cpd1/1.0.0@official/cppdev"),
                dependencies=[ConanPackageReferenceWithSemanticVersion("dep/2.0.0@official/cppdev")],
                cpp_standard="c++20",
            ),
        ]
        with create_conan_test_env(tmp_path / "conan", server.http_port, TEST_PACKAGES) as conan_test_env:
            yield conan_test_env

@pytest.mark.conan_remote
def test_conan_remote_login(conan_test_environment: ConanTestEnv) -> None:
    conan_remote_login(CONAN_REMOTE, conan_test_environment.server.user, conan_test_environment.server.password)
    

@pytest.mark.conan_remote
@pytest.mark.usefixtures("conan_test_environment")
def test_conan_list() -> None:
    result = conan_list(CONAN_REMOTE, "cpd")
    assert len(result) == 1
    assert ConanPackageReferenceWithSemanticVersion("cpd/1.0.0@official/cppdev") in result


@pytest.mark.conan_remote
def test_conan_graph_buildorder(tmp_path: Path, conan_test_environment: ConanTestEnv) -> None:
    conanfile_path = tmp_path / "conanfile.txt"
    conanfile_path.write_text(dedent("""
        [requires]
        cpd/1.0.0@official/cppdev
        """)
    )
    graph_build_order = conan_graph_buildorder(conanfile_path, conan_test_environment.profile, conan_test_environment.construct_conan_settings())
    assert len(graph_build_order.order) == 2
    assert len(graph_build_order.order[0]) == 1
    dep_recipe = graph_build_order.order[0][0]
    assert dep_recipe.ref.startswith("dep/1.0.0@official/cppdev")

    assert len(graph_build_order.order[1]) == 1
    cpd_recipe = graph_build_order.order[1][0]
    assert cpd_recipe.ref.startswith("cpd/1.0.0@official/cppdev")
    assert len(cpd_recipe.depends) == 1
    assert cpd_recipe.depends[0].startswith("dep/1.0.0@official/cppdev")
        

@pytest.mark.conan_remote
def test_conan_graph_buildorder_dependency_does_not_exist(tmp_path: Path, conan_test_environment: ConanTestEnv) -> None:
    conanfile_path = tmp_path / "conanfile.txt"
    conanfile_path.write_text(dedent("""
        [requires]
        cpd/0.0.0@official/cppdev
        """)
    )

    with pytest.raises(ConanCommandException, match="unable to find package") as e:
        conan_graph_buildorder(conanfile_path, conan_test_environment.profile, conan_test_environment.construct_conan_settings())


@pytest.mark.conan_remote
def test_conan_graph_buildorder_multiple_dependencies(tmp_path: Path, conan_test_environment: ConanTestEnv) -> None:
    conanfile_path = tmp_path / "conanfile.txt"
    conanfile_path.write_text(dedent("""
        [requires]
        cpd/[>=0.0.0]@official/cppdev
        cpd1/[<2.0.0]@official/cppdev                                     
        """)
    )

    with pytest.raises(ConanCommandException, match="version conflict") as e:
        conan_graph_buildorder(conanfile_path, conan_test_environment.profile, conan_test_environment.construct_conan_settings())