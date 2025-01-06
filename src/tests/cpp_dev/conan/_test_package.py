# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from unittest.mock import patch

from cpp_dev.common.types import SemanticVersion
from cpp_dev.conan.package import get_available_versions
from cpp_dev.dependency.conan.types import ConanPackageReference


def test_get_available_versions() -> None:
    with patch("cpp_dev.conan.package.conan_list", return_value={
        ConanPackageReference("cpd/1.0.0@official/cppdev"): {},
        ConanPackageReference("cpd/2.0.0@custom/cppdev"): {},
        ConanPackageReference("cpd/3.0.0@official/cppdev"): {},
    }):
        assert get_available_versions("official", "cpd") == [
            SemanticVersion("3.0.0"),
            SemanticVersion("1.0.0"),
        ]