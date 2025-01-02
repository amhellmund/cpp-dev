# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.common.version import SemanticVersionWithOptionalParts
from cpp_dev.dependency.specifier import DependencySpecifier
from cpp_dev.dependency.types import DependencySpecifierParts, VersionSpecBound, VersionSpecBoundOperand


def test_dependency_specifier() -> None:
    specifier = DependencySpecifier("official/cpd[>1.0.0]")
    assert specifier.repository == "official"
    assert specifier.name == "cpd"
    assert isinstance(specifier.version_spec, list)
    assert len(specifier.version_spec) == 1

    assert specifier.version_spec[0] == VersionSpecBound(
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
    specifier = DependencySpecifier("official/cpd[>1.0.0]")
    roundtrip_specifier = DependencySpecifier.from_parts(
        DependencySpecifierParts(specifier.repository, specifier.name, specifier.version_spec)
    )
    assert specifier == roundtrip_specifier
