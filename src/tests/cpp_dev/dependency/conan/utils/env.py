# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from collections.abc import Generator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from cpp_dev.common.types import CppStandard
from cpp_dev.common.utils import ensure_dir_exists
from cpp_dev.dependency.conan.command_wrapper import conan_create, conan_upload
from cpp_dev.dependency.conan.setup import CONAN_REMOTE, initialize_conan
from cpp_dev.dependency.conan.types import ConanPackageReference
from cpp_dev.dependency.conan.utils import conan_env
from tests.cpp_dev.dependency.conan.utils.server import (
    ConanServer, launch_conan_test_server)

###############################################################################
# Public API                                                                ###
###############################################################################

FileSpec = Mapping[Path, str]

@dataclass
class ConanTestPackage:
    ref: ConanPackageReference
    dependencies: list[ConanPackageReference]
    cpp_standard: CppStandard
    bin_files: FileSpec | None = None
    lib_files: FileSpec | None = None
    include_files: FileSpec | None = None


class ConanTestEnv:
    """A Conan environment for testing."""

    def __init__(self, conan_home_dir: Path, profile: str, server: ConanServer) -> None:
        self._conan_home_dir = conan_home_dir
        self._package_dir =  conan_home_dir / ".conan_package_creation"
        ensure_dir_exists(self._package_dir)
        self._profile = profile
        self._server = server

    def create_and_upload_packages(self, packages: list[ConanTestPackage]) -> None:
        """Create and upload a Conan package for testing."""
        for package in packages:
            _create_and_upload_conan_package(self._package_dir, package, self._profile)

    @property
    def conan_home_dir(self) -> Path:
        """Return the base directory of the Conan environment."""
        return self._conan_home_dir

    @property
    def profile(self) -> str:
        """Return the profile used for testing."""
        return self._profile
    
    @property
    def server(self) -> ConanServer:
        """Return the server used for testing."""
        return self._server


@contextmanager
def create_conan_test_env(base_dir: Path, server_http_port: int, packages: list[ConanTestPackage]) -> Generator[ConanTestEnv]:
    """Create a Conan environment for testing."""
    
    # create the home for the conan server
    conan_server_dir = base_dir / "server"
    ensure_dir_exists(conan_server_dir)
    with launch_conan_test_server(conan_server_dir, server_http_port) as server:
        # create the home for the conan client
        conan_home_dir = base_dir / "conan_home"
        ensure_dir_exists(conan_home_dir)
        source_config_path, profile = _create_conan_source_config(conan_home_dir, server_http_port)
        initialize_conan(conan_home_dir, source_config_path)

        with conan_env(conan_home_dir):
            conan_test_env = ConanTestEnv(conan_home_dir, profile, server)
            conan_test_env.create_and_upload_packages(packages)
            yield conan_test_env


###############################################################################
# Implementation                                                            ###
###############################################################################

def _create_conan_source_config(conan_dir: Path, server_http_port: int) -> tuple[Path, str]:
    source_config_path = conan_dir / ".source_config"
    ensure_dir_exists(source_config_path)

    PROFILE_NAME = "test"
    test_profile_path = source_config_path / "profiles" / PROFILE_NAME
    ensure_dir_exists(test_profile_path.parent)
    test_profile_path.write_text(dedent(
        """
        [settings]
        arch=test
        build_type=Test
        os=Linux
        os.distro=test
        """
    ))

    settings_path = source_config_path / "settings.yml"
    settings_path.write_text(dedent(
        """
        os:
          Linux:
            distro: ["test"]   
        arch: [test]
        compiler:
          test:
        build_type: [Test]
        """
    ))

    remotes_path = source_config_path / "remotes.json"
    remotes_path.write_text(json.dumps({
        "remotes": [
            {
                "name": CONAN_REMOTE,
                "url": f"http://localhost:{server_http_port}/",
                "verify_ssl": False,
            }
        ]
    }))

    return source_config_path, PROFILE_NAME


def _create_and_upload_conan_package(base_dir: Path, package: ConanTestPackage, profile: str) -> None:
    package_dir = base_dir / f"{package.ref.name}_{package.ref.version}"
    ensure_dir_exists(package_dir)

    conanfile_path = package_dir / "conanfile.py"

    requirements = ",".join([f"\"{dep}\"" for dep in package.dependencies])
    conanfile_path.write_text(dedent(
        """
        from conan import ConanFile

        class TestConan(ConanFile):
            name = "{name}"
            user = "{user}"
            channel = "cppdev"
            version = "{version}"

            {requirements}
        """.format(
            name=package.ref.name,
            user=package.ref.user,
            version=package.ref.version,
            requirements=f"requires = {requirements}" if package.dependencies else ""
        )
    ))
    conan_create(package_dir, profile)
    conan_upload(package.ref, CONAN_REMOTE)