# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from cpp_dev.common.types import SemanticVersion
from cpp_dev.common.utils import create_tmp_dir
from cpp_dev.project.dependency.types import PackageDependency
from cpp_dev.tool.init import get_conan_home_dir

from .command_wrapper import conan_list
from .setup import CONAN_REMOTE
from .types import ConanPackageReference
from .utils import conan_env, create_conanfile

###############################################################################
# Public API                                                                ###
###############################################################################

def get_available_versions(repository: str, name: str) -> list[SemanticVersion]:
    """Retrieve available versions for a package represented by repository (aka. Conan user) and name.
    
    Result:
        The versions get sorted in reverse order such that the latest version is first in the list.
    """
    with conan_env(get_conan_home_dir()):
        package_references = _retrieve_conan_package_references(repository, name)
        available_versions = sorted([ref.version for ref in package_references], reverse=True)
        return available_versions
        

def compute_dependency_graph(package_refs: list[PackageDependency]) -> None:
    """Retrieve the dependency graph for the given package dependencies."""
    with conan_env(get_conan_home_dir()):
        with create_tmp_dir() as tmp_dir:
            conanfile_path = create_conanfile(tmp_dir, package_refs)
            



###############################################################################
# Implementation                                                            ###
###############################################################################

def _retrieve_conan_package_references(repository: str, name: str) -> list[ConanPackageReference]:
    package_data = conan_list(CONAN_REMOTE, name)
    package_references = [
        ref
        for ref in package_data.keys()
        if ref.user == repository
    ]
    return package_references



