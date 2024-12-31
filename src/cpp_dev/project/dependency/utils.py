# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from copy import deepcopy

from cpp_dev.conan.package import get_available_versions
from cpp_dev.tool.init import get_conan_home_dir

from .parts import VersionSpecBound, VersionSpecBoundOperand
from .types import PackageDependency

###############################################################################
# Public API                                                                ###
###############################################################################


DEFAULT_REPOSITORY = "official"


def refine_package_dependencies(deps: list[PackageDependency]) -> list[PackageDependency]:
    """Refine the package dependencies in case of defaults were chosen.

    The refinement includes (in order):
        o Default repository 'official'
        o Latest resolved version in case of 'latest'

    This step is performed to assure that package dependencies with 'latest' do not get an older version
    than the latest one at the time of resolution. This is important in case a versions gets removed.
    """
    updated_deps = []
    for dep in deps:
        parts = deepcopy(dep.parts)
        if parts.repository is None:
            parts.repository = DEFAULT_REPOSITORY
        if parts.version_spec == "latest":
            available_versions = get_available_versions(get_conan_home_dir(), parts.repository, parts.name)
            if len(available_versions) == 0:
                raise ValueError(f"No available versions for package {dep.name} at repository {parts.repository}.")
            parts.version_spec = [
                VersionSpecBound(
                    operand=VersionSpecBoundOperand.GREATER_THAN_OR_EQUAL,
                    version=available_versions[0],
                )
            ]
        updated_deps.append(PackageDependency.from_parts(parts))
    return updated_deps
