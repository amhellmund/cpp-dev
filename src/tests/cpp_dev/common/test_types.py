# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from cpp_dev.common.types import SemanticVersion


def test_semantic_version_ok() -> None:
    SemanticVersion("1.2.3")
    SemanticVersion("10.20.30")


@pytest.mark.parametrize("version", ["1.2", "abc", "a.b.c", "1.2.3.4"])
def test_semantic_version_fail(version: str) -> None:
    with pytest.raises(ValueError, match="Invalid semantic version"):
        SemanticVersion(version)
