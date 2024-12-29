# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.dependency.parts import SemanticVersionWithOptionalParts, VersionSpecBound, VersionSpecBoundOperand
from cpp_dev.dependency.types import PackageDependency


def test_package_dependency() -> None:
    parts = PackageDependency("official/cpd[>1.0.0]").parts
    assert parts.repository == "official"
    assert parts.name == "cpd"
    assert isinstance(parts.version_spec, list)
    assert len(parts.version_spec) == 1

    assert parts.version_spec[0] == VersionSpecBound(
        operand=VersionSpecBoundOperand.GREATER_THAN,
        version=SemanticVersionWithOptionalParts(1, 0, 0),
    )
