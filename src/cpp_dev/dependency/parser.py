# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

from cpp_dev.common.types import SemanticVersion
from cpp_dev.common.utils import assert_is_not_none

from .parts import (
    PackageDependencyParts,
    SemanticVersionWithOptionalParts,
    VersionSpecBound,
    VersionSpecBoundOperand,
    VersionSpecType,
    VersionSpecTypeLatest,
)

###############################################################################
# Public API                                                                ###
###############################################################################


class DependencyParserError(Exception):
    """Exception for raising issues during dependency parsing."""


def parse_dependency_string(dep_str: str) -> PackageDependencyParts:
    """Parse a package dependency string into its components.

    It raises a DependencyParserError in case of an invalid format or syntax error.
    """
    tokens = _tokenize(dep_str)
    token_provider = _TokenProvider(tokens=tokens)
    return _parse_spec(token_provider)


###############################################################################
# Implementation                                                            ###
###############################################################################


class _TokenType(Enum):
    LATEST = 0
    IDENTIFIER = 1
    NUMBER = 2
    SLASH = 3
    LEFT_BRACKET = 4
    RIGHT_BRACKET = 5
    COMMA = 6
    DOT = 7
    LESS = 8
    LESS_THAN_OR_EQUAL = 9
    GREATER = 10
    GREATER_THAN_OR_EQUAL = 11


@dataclass
class _Token:
    type: _TokenType
    value: str


def _tokenize(dep_str: str) -> list[_Token]:
    token_specification = [
        ("LATEST", r"latest"),
        ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("NUMBER", r"\d+"),
        ("SLASH", r"/"),
        ("DOT", r"\."),
        ("LEFT_BRACKET", r"\["),
        ("RIGHT_BRACKET", r"\]"),
        ("COMMA", r","),
        ("LESS_THAN_OR_EQUAL", r"<="),
        ("LESS", r"<"),
        ("GREATER_THAN_OR_EQUAL", r">="),
        ("GREATER", r">"),
    ]

    token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    get_token = re.compile(token_regex).match
    pos = 0
    tokens = []
    while pos < len(dep_str):
        match = get_token(dep_str, pos)
        if match is not None:
            type_ = assert_is_not_none(match.lastgroup)
            value = match.group(type_)
            tokens.append(_Token(_TokenType[type_], value))
            pos = match.end()
        else:
            raise DependencyParserError(f"Unexpected character at position {pos}: {dep_str[pos]}")
    return tokens


class _TokenProvider:
    def __init__(self, tokens: list[_Token]) -> None:
        self._tokens = tokens
        self._pos = 0

    def current_has_token_types(self, *expected_types: _TokenType) -> bool:
        token = self.current()
        if token is not None:
            return token.type in expected_types
        return False

    def assert_token_type_and_consume(self, expected_type: _TokenType | list[_TokenType]) -> _Token:
        """Check that the current token has the expected type.

        Raise a value error if the current token is None or has a different type.
        """
        if isinstance(expected_type, _TokenType):
            expected_type = [expected_type]
        token = self.current()
        if token is None:
            raise DependencyParserError("Unexpected end of input, expected token of type {expected_type}.")
        if token.type not in expected_type:
            raise DependencyParserError(
                f"Expected token of type {expected_type}, got {token.type} with value {token.value}.",
            )
        self._consume()
        return token

    def consume_if_token_type(self, expected_type: _TokenType) -> bool:
        """Check that the current token has either the expected type or EOF is reached.

        Return True if the current token has the expected type, False if EOF is reached.
        Raise a value error if the current token has a different type.
        """
        token = self.current()
        if token is not None and token.type == expected_type:
            self._consume()
            return True
        return False

    def assert_eof(self) -> None:
        if self._pos < len(self._tokens):
            raise DependencyParserError(f"Expected EOF, but got {self._tokens[self._pos].value}.")

    def current(self) -> _Token | None:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _consume(self) -> None:
        self._pos += 1


def _parse_spec(tokens: _TokenProvider) -> PackageDependencyParts:
    repository, name = _parse_repository_and_name(tokens)
    version_spec = _parse_version_spec(tokens)
    tokens.assert_eof()
    return PackageDependencyParts(repository, name, version_spec)


def _parse_repository_and_name(tokens: _TokenProvider) -> tuple[str | None, str]:
    token_repo_or_name = tokens.assert_token_type_and_consume(_TokenType.IDENTIFIER)
    if tokens.consume_if_token_type(_TokenType.SLASH):
        token_name = tokens.assert_token_type_and_consume(_TokenType.IDENTIFIER)
        return token_repo_or_name.value, token_name.value
    return None, token_repo_or_name.value


_COMPARISON_OPERATOR_TOKENS_TYPES = [
    _TokenType.GREATER,
    _TokenType.GREATER_THAN_OR_EQUAL,
    _TokenType.LESS,
    _TokenType.LESS_THAN_OR_EQUAL,
]


def _parse_version_spec(tokens: _TokenProvider) -> VersionSpecType:
    version_spec: VersionSpecType = "latest"
    if tokens.consume_if_token_type(_TokenType.LEFT_BRACKET):
        if tokens.current_has_token_types(_TokenType.LATEST):
            version_spec = _parse_latest(tokens)
        elif tokens.current_has_token_types(_TokenType.NUMBER):
            version_spec = _parse_semantic_version(tokens)
        elif tokens.current_has_token_types(*_COMPARISON_OPERATOR_TOKENS_TYPES):
            version_spec = _parse_version_bounds(tokens)
        else:
            raise DependencyParserError("Expected latest, semantic version or version bounds within brackets.")
        tokens.assert_token_type_and_consume(_TokenType.RIGHT_BRACKET)
    return version_spec


def _parse_latest(tokens: _TokenProvider) -> VersionSpecTypeLatest:
    """Parse a latest.

    This function assumes the latest token has not yet been consumed yet. Note: this function only exists for
    symmetry reasons in the parent function.
    """
    tokens.assert_token_type_and_consume(_TokenType.LATEST)
    return "latest"


def _parse_semantic_version(tokens: _TokenProvider) -> SemanticVersion:
    """Parse a semantic version.

    This function assumes the leading major number has not yet been consumed yet.
    """
    major_token = tokens.assert_token_type_and_consume(_TokenType.NUMBER)
    tokens.assert_token_type_and_consume(_TokenType.DOT)
    minor_token = tokens.assert_token_type_and_consume(_TokenType.NUMBER)
    tokens.assert_token_type_and_consume(_TokenType.DOT)
    patch_token = tokens.assert_token_type_and_consume(_TokenType.NUMBER)

    return SemanticVersion(f"{major_token.value}.{minor_token.value}.{patch_token.value}")


def _parse_version_bounds(tokens: _TokenProvider) -> list[VersionSpecBound]:
    """Parse a version bounds.

    This function assumes the comparison operand has not yet been consumed yet.
    """
    version_spec_bounds = []
    while comp_operator_token := tokens.assert_token_type_and_consume(_COMPARISON_OPERATOR_TOKENS_TYPES):
        semantic_version_with_opts = _parse_semantic_version_with_optionals(tokens)
        version_spec_bounds.append(
            VersionSpecBound(
                operand=VersionSpecBoundOperand(comp_operator_token.value),
                version=semantic_version_with_opts,
            ),
        )
        if not tokens.consume_if_token_type(_TokenType.COMMA):
            break

    return version_spec_bounds


def _parse_semantic_version_with_optionals(tokens: _TokenProvider) -> SemanticVersionWithOptionalParts:
    """Parse a semantic version.

    This function assumes the leading major number not being consumed yet.
    """

    def convert_next_token_to_int() -> int:
        return int(tokens.assert_token_type_and_consume(_TokenType.NUMBER).value)

    major_number = convert_next_token_to_int()
    minor_number = None
    patch_number = None
    if tokens.consume_if_token_type(_TokenType.DOT):
        minor_number = convert_next_token_to_int()
        if tokens.consume_if_token_type(_TokenType.DOT):
            patch_number = convert_next_token_to_int()
    return SemanticVersionWithOptionalParts(
        major=major_number,
        minor=minor_number,
        patch=patch_number,
    )
