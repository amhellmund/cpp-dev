# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

from cpp_dev.common.types import SemanticVersion
from cpp_dev.conan.command_wrapper import conan_list
from cpp_dev.conan.setup import CONAN_REMOTE
from cpp_dev.conan.types import ConanPackageReference
from cpp_dev.conan.utils import conan_env

###############################################################################
# Public API                                                                ###
###############################################################################

def get_available_versions(conan_home: Path, repository: str, name: str) -> list[SemanticVersion]:
    """Retrieve available versions for a package represented by repository (aka. Conan user) and name.
    
    Result:
        The versions get sorted in reverse order such that the latest version is first in the list.
    """
    with conan_env(conan_home):
        package_references = _retrieve_conan_package_references(repository, name)
        available_versions = sorted([ref.version for ref in package_references], reverse=True)
        return available_versions
        




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