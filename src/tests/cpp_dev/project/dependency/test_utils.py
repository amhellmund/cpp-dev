# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Mapping
from unittest.mock import patch

from cpp_dev.conan.types import ConanPackageReference
from cpp_dev.dependency.types import PackageDependency
from cpp_dev.project.dependency.utils import refine_package_dependencies


def conan_list_side_effect(_remote: str, name: str) -> Mapping[ConanPackageReference, dict]:
    if name == "cpd":
        return {
            ConanPackageReference("cpd/1.0.0@official/cppdev"): {},
            ConanPackageReference("cpd/2.0.0@official/cppdev"): {},
        }
    if name == "cpd2":
        return {
            ConanPackageReference("cpd2/3.0.0@official/cppdev"): {},
            ConanPackageReference("cpd2/3.0.0@official/cppdev"): {},
        }
    if name == "other":
        return {
            ConanPackageReference("other/2.0.0@custom/cppdev"): {},
        }
    return {}


def test_refine_package_dependencies() -> None:
    with patch("cpp_dev.conan.package.conan_list", side_effect=conan_list_side_effect):
        refined_deps = refine_package_dependencies(
            [
                PackageDependency("cpd"),
                PackageDependency("custom/other[latest]"),
                PackageDependency("cpd2[3.0.0]"),
            ]
        )
        assert refined_deps == [
            PackageDependency("official/cpd[>=2.0.0]"),
            PackageDependency("custom/other[>=2.0.0]"),
            PackageDependency("official/cpd2[3.0.0]"),
        ]
