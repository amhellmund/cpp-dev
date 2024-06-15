# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from cpp_dev.common.types import SemanticVersion, PackageRef


def test_semantic_version():
    SemanticVersion("1.2.3")
    SemanticVersion("10.20.30")

    with pytest.raises(ValueError):
        SemanticVersion("1.2")
        SemanticVersion("abc")
        SemanticVersion("a.b.c")
        SemanticVersion("1.2.3.4")


def test_package_ref():
    assert PackageRef("repo-name-1.2.3").unpack == (
        "repo",
        "name",
        SemanticVersion("1.2.3"),
    )

    with pytest.raises(ValueError):
        PackageRef("repo1-name1-1.2")
        PackageRef("repo-name")
        PackageRef("repo-1.2.3")
        PackageRef("name-1.2.3")
        PackageRef("name")
        PackageRef("repo")
        PackageRef("1.2.3")
