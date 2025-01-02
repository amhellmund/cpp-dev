# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import pytest

from cpp_dev.common.types import SemanticVersion, SemanticVersionWithOptionalParts
from cpp_dev.dependency.specifier_parser import DependencyParserError, parse_dependency_string
from cpp_dev.dependency.types import DependencySpecifierParts, VersionSpecBound, VersionSpecBoundOperand


@pytest.mark.parametrize(
    ("dep_str", "expected"),
    [
        ("cpd", DependencySpecifierParts(repository=None, name="cpd", version_spec="latest")),
        ("repo/cpd", DependencySpecifierParts(repository="repo", name="cpd", version_spec="latest")),
        ("repo/cpd[latest]", DependencySpecifierParts(repository="repo", name="cpd", version_spec="latest")),
        (
            "cpd[1.2.3]",
            DependencySpecifierParts(repository=None, name="cpd", version_spec=SemanticVersion("1.2.3")),
        ),
        (
            "cpd[>1.0.0]",
            DependencySpecifierParts(
                repository=None,
                name="cpd",
                version_spec=[
                    VersionSpecBound(
                        operand=VersionSpecBoundOperand.GREATER_THAN,
                        version=SemanticVersionWithOptionalParts(1, 0, 0),
                    ),
                ],
            ),
        ),
        (
            "cpd[>=1.0]",
            DependencySpecifierParts(
                repository=None,
                name="cpd",
                version_spec=[
                    VersionSpecBound(
                        operand=VersionSpecBoundOperand.GREATER_THAN_OR_EQUAL,
                        version=SemanticVersionWithOptionalParts(1, 0, None),
                    ),
                ],
            ),
        ),
        (
            "cpd[<1]",
            DependencySpecifierParts(
                repository=None,
                name="cpd",
                version_spec=[
                    VersionSpecBound(
                        operand=VersionSpecBoundOperand.LESS_THAN,
                        version=SemanticVersionWithOptionalParts(1, None, None),
                    ),
                ],
            ),
        ),
        (
            "cpd[>1,<=2.0]",
            DependencySpecifierParts(
                repository=None,
                name="cpd",
                version_spec=[
                    VersionSpecBound(
                        operand=VersionSpecBoundOperand.GREATER_THAN,
                        version=SemanticVersionWithOptionalParts(1, None, None),
                    ),
                    VersionSpecBound(
                        operand=VersionSpecBoundOperand.LESS_THAN_OR_EQUAL,
                        version=SemanticVersionWithOptionalParts(2, 0, None),
                    ),
                ],
            ),
        ),
    ],
)
def test_dependency_specifier_parser_ok(dep_str: str, expected: DependencySpecifierParts) -> None:
    assert parse_dependency_string(dep_str) == expected


@pytest.mark.parametrize(
    "dep_str",
    [
        "",
        "[]",
        "/[]",
        "repo/cpd/another",
        "[latest]",
        "cpd[latest1]",
        "cpd[1.0]",
        "cpd[1]",
        "cpd[1.0.0.0]",
        "cpd[]",
        "cpd[=1.0.0]",
        "cpd[>=,<=]",
        "cpd[1.x.0]",
    ],
)
def test_dependency_specifier_parser_fail(dep_str: str) -> None:
    with pytest.raises(DependencyParserError):
        parse_dependency_string(dep_str)
