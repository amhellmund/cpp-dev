# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.provider import DependencyIdentifier


def test_dependency_identifier_ok() -> None:
    dep_str = "repo/name/1.2.3"
    dep_id = DependencyIdentifier.from_str(dep_str)

    assert dep_id.repository == "repo"
    assert dep_id.name == "name"
    assert dep_id.version == SemanticVersion("1.2.3")

    assert str(dep_id) == dep_str


@pytest.mark.parametrize("dep_id_str", ["repo/name", "repo/name/1.2", "repo/name/1.2.3.4"])
def test_dependency_identifier_fail(dep_id_str: str) -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        DependencyIdentifier.from_str(dep_id_str)
