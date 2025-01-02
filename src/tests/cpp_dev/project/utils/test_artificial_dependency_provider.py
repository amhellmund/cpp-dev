# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.provider import Dependency, DependencyIdentifier
from tests.cpp_dev.project.utils.artificial_dependency_provider import ArtificialDependencyProvider


def test_available_versions() -> None:
    provider = ArtificialDependencyProvider(
        [
            Dependency(id=DependencyIdentifier.from_str("official/gtest/1.0.0"), cpp_standard="c++17", deps=[]),
            Dependency(id=DependencyIdentifier.from_str("official/gtest/1.10.0"), cpp_standard="c++17", deps=[]),
            Dependency(id=DependencyIdentifier.from_str("custom/gtest/1.11.0"), cpp_standard="c++17", deps=[]),
        ]
    )
    assert provider.fetch_versions("official", "gtest") == [
        SemanticVersion("1.10.0"),
        SemanticVersion("1.0.0"),
    ]
    assert provider.fetch_versions("custom", "gtest") == [SemanticVersion("1.11.0")]
