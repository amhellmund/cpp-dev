# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.common.version import SemanticVersionWithOptionalParts
from cpp_dev.dependency.specifier import DependencySpecifier
from cpp_dev.dependency.types import DependencySpecifierParts, VersionSpecBound, VersionSpecBoundOperand


def test_dependency_specifier() -> None:
    parts = DependencySpecifier("official/cpd[>1.0.0]").parts
    assert parts.repository == "official"
    assert parts.name == "cpd"
    assert isinstance(parts.version_spec, list)
    assert len(parts.version_spec) == 1

    assert parts.version_spec[0] == VersionSpecBound(
        operand=VersionSpecBoundOperand.GREATER_THAN,
        version=SemanticVersionWithOptionalParts(1, 0, 0),
    )


def test_dependency_specifier_from_parts() -> None:
    parts = DependencySpecifierParts(
        "official",
        "cpd",
        [
            VersionSpecBound(
                operand=VersionSpecBoundOperand.GREATER_THAN,
                version=SemanticVersionWithOptionalParts(1, 0, 0),
            )
        ],
    )
    dependency = DependencySpecifier.from_parts(parts)
    assert dependency.root == "official/cpd[>1.0.0]"


def test_dependency_specifier_parts_roundtrip() -> None:
    dependency = DependencySpecifier("official/cpd[>1.0.0]")
    roundtrip_dependency = DependencySpecifier.from_parts(dependency.parts)
    assert dependency == roundtrip_dependency
