# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import os
from pathlib import Path

import pytest

from cpp_dev.conan.utils import (CONAN_HOME_ENV_VAR,
                                 compose_conan_package_reference, conan_env,
                                 create_conanfile)
from cpp_dev.project.dependency.types import PackageDependency


def test_conan_env() -> None:
    if CONAN_HOME_ENV_VAR in os.environ:
        del os.environ[CONAN_HOME_ENV_VAR]
    with conan_env("conan"):
        assert CONAN_HOME_ENV_VAR in os.environ
        assert os.environ[CONAN_HOME_ENV_VAR] == "conan"
    assert CONAN_HOME_ENV_VAR not in os.environ


def test_create_conanfile(tmp_path: Path) -> None:
    package_deps = [
        PackageDependency("official/cpd[1.0.0]"),
        PackageDependency("custom/other[>2.0.0]"),
        PackageDependency("custom/other2[>=3.0.0,<4.0.0]"),
    ]
    conanfile_path = create_conanfile(tmp_path, package_deps)
    assert conanfile_path.exists()
    assert conanfile_path.is_file()
    conanfile_content_as_lines = conanfile_path.read_text().strip().splitlines()
    assert conanfile_content_as_lines[0] == "[requires]"
    assert conanfile_content_as_lines[1] == "cpd/1.0.0@official/cppdev"
    assert conanfile_content_as_lines[2] == "other/[>2.0.0]@custom/cppdev"
    assert conanfile_content_as_lines[3] == "other2/[>=3.0.0 <4.0.0]@custom/cppdev"


@pytest.mark.parametrize(("ref", "expected_conan_ref"), [
    ("official/cpd[1.0.0]", "cpd/1.0.0@official/cppdev"),
    ("custom/other[>2.0.0]", "other/[>2.0.0]@custom/cppdev"),
    ("custom/other2[>=3.0.0,<4.0.0]", "other2/[>=3.0.0 <4.0.0]@custom/cppdev"),
])
def test_compose_conan_package_reference(ref: str, expected_conan_ref) -> None:
    conan_ref = compose_conan_package_reference(PackageDependency(ref))
    assert conan_ref == expected_conan_ref