# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from collections.abc import Mapping
from pathlib import Path

import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.conan.types import ConanPackageReference
from cpp_dev.dependency.provider import Dependency, DependencyIdentifier, DependencyProvider
from cpp_dev.dependency.specifier import DependencySpecifier
from cpp_dev.project.config import ProjectConfig, load_project_config
from cpp_dev.project.core import _refine_package_dependencies, setup_project
from cpp_dev.project.lockfile import load_lock_file
from cpp_dev.project.path_composition import compose_project_config_file, compose_project_lock_file
from tests.cpp_dev.project.utils.artificial_dependency_provider import ArtificialDependencyProvider


@pytest.fixture
def dep_provider() -> DependencyProvider:
    return ArtificialDependencyProvider(
        dependencies=[
            Dependency(id=DependencyIdentifier.from_str("official/llvm/1.0.0"), cpp_standard="c++17", deps=[]),
            Dependency(id=DependencyIdentifier.from_str("official/gtest/1.0.0"), cpp_standard="c++17", deps=[]),
        ]
    )


def test_setup_project(tmp_path: Path, dep_provider: DependencyProvider) -> None:
    project_config = ProjectConfig(
        name="test_package",
        version=SemanticVersion("1.0.0"),
        std="c++17",
        author="author",
        license="license",
        description="description",
        dependencies=[],
        dev_dependencies=[],
        cpd_dependencies=[],
    )

    project = setup_project(project_config, dep_provider, parent_dir=tmp_path)

    assert project.project_dir.exists()
    assert project.project_dir == tmp_path / project_config.name

    assert compose_project_config_file(project.project_dir).exists()

    config = load_project_config(project.project_dir)
    assert config == project_config

    assert len(config.dependencies) == 0
    assert len(config.dev_dependencies) == 0
    assert len(config.cpd_dependencies) == 0

    assert compose_project_lock_file(project.project_dir).exists()
    locked_dependencies = load_lock_file(project.project_dir)
    assert len(locked_dependencies.packages) == 0

    assert (project.project_dir / "include" / project_config.name / f"{project_config.name}.hpp").exists()
    assert (project.project_dir / "src" / f"{project_config.name}.cpp").exists()
    assert (project.project_dir / "src" / f"{project_config.name}.test.cpp").exists()


def conan_list_side_effect(_remote: str, name: str) -> Mapping[ConanPackageReference, dict]:
    if name == "cpd":
        return {
            ConanPackageReference("cpd/1.0.0@official/cppdev"): {},
            ConanPackageReference("cpd/2.0.0@official/cppdev"): {},
        }
    if name == "cpd2":
        return {
            ConanPackageReference("cpd2/3.0.0@official/cppdev"): {},
            ConanPackageReference("cpd2/3.0.0@official/cppdev"): {},
        }
    if name == "other":
        return {
            ConanPackageReference("other/2.0.0@custom/cppdev"): {},
        }
    return {}


def test_refine_package_dependencies(dep_provider: DependencyProvider) -> None:
    refined_deps = _refine_package_dependencies(
        dep_provider,
        [
            DependencySpecifier("llvm"),
            DependencySpecifier("official/llvm[latest]"),
            DependencySpecifier("gtest[3.0.0]"),
        ],
    )
    assert refined_deps == [
        DependencySpecifier("official/llvm[>=1.0.0]"),
        DependencySpecifier("official/llvm[>=1.0.0]"),
        DependencySpecifier("official/gtest[3.0.0]"),
    ]
