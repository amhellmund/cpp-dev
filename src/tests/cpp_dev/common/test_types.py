# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

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
