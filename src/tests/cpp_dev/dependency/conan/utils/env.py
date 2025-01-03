# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent

from cpp_dev.common.utils import ensure_dir_exists
from cpp_dev.conan.command_wrapper import conan_create, conan_upload
from cpp_dev.conan.setup import CONAN_REMOTE, initialize_conan
from cpp_dev.conan.types import ConanPackageReference
from cpp_dev.conan.utils import conan_env

###############################################################################
# Public API                                                                ###
###############################################################################

class ConanTestEnv:
    """A Conan environment for testing."""

    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir / ".conan_test_env"
        ensure_dir_exists(self._base_dir)

    def create_and_upload_package(self, ref: ConanPackageReference, dependencies: list[ConanPackageReference]) -> None:
        """Create and upload a Conan package for testing."""
        _create_and_upload_conan_package(self._base_dir, ref, dependencies)


@contextmanager
def create_conan_env(conan_dir: Path, server_http_port: int) -> Generator[ConanTestEnv]:
    """Create a Conan environment for testing."""
    ensure_dir_exists(conan_dir)
    source_config_path = _create_conan_source_config(conan_dir, server_http_port)
    initialize_conan(conan_dir, source_config_path)
    with conan_env(conan_dir):
        yield ConanTestEnv(conan_dir)


###############################################################################
# Implementation                                                            ###
###############################################################################

def _create_conan_source_config(conan_dir: Path, server_http_port: int) -> Path:
    source_config_path = conan_dir / ".source_config"
    ensure_dir_exists(source_config_path)

    test_profile_path = source_config_path / "profiles" / "test"
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

    return source_config_path


def _create_and_upload_conan_package(base_dir: Path, ref: ConanPackageReference, dependencies: list[ConanPackageReference]) -> None:
    package_dir = base_dir / f"{ref.name}_{ref.version}"
    ensure_dir_exists(package_dir)

    conanfile_path = package_dir / "conanfile.py"

    requirements = ",".join([f"\"{dep}\"" for dep in dependencies])
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
            name=ref.name,
            user=ref.user,
            version=ref.version,
            requirements=f"requires = {requirements}" if dependencies else ""
        )
    ))
    conan_create(package_dir, "test")
    conan_upload(ref, CONAN_REMOTE)