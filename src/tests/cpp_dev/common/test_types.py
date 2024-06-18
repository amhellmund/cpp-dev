# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from cpp_dev.common.types import SemanticVersion


def test_semantic_version():
    SemanticVersion("1.2.3")
    SemanticVersion("10.20.30")

    with pytest.raises(ValueError):
        SemanticVersion("1.2")
        SemanticVersion("abc")
        SemanticVersion("a.b.c")
        SemanticVersion("1.2.3.4")
