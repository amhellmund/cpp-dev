# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from cpp_dev.common.version import SemanticVersion, SemanticVersionWithOptionalParts


def test_semantic_version_ok() -> None:
    version = SemanticVersion("1.2.3")
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3

    version = SemanticVersion("10.20.30")
    assert version.major == 10
    assert version.minor == 20
    assert version.patch == 30


@pytest.mark.parametrize("version", ["1.2", "abc", "a.b.c", "1.2.3.4", "1.-2.3", "1.2.abc"])
def test_semantic_version_fail(version: str) -> None:
    with pytest.raises(ValueError, match="Invalid semantic version"):
        SemanticVersion(version)


def test_semantic_version_from_parts() -> None:
    version = SemanticVersion.from_parts(1, 2, 3)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3


def test_semantic_version_with_optional_parts_ok() -> None:
    version = SemanticVersionWithOptionalParts(1, 2, 3)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3

    version = SemanticVersionWithOptionalParts(1, 2, None)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch is None

    version = SemanticVersionWithOptionalParts(1, None, None)
    assert version.major == 1
    assert version.minor is None
    assert version.patch is None


def test_semantic_version_with_optional_parts_fail() -> None:
    with pytest.raises(ValueError, match="Cannot specify a patch version without a minor version"):
        SemanticVersionWithOptionalParts(1, None, 3)
