# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, RootModel

from cpp_dev.common.process import run_command, run_command_assert_success
from cpp_dev.dependency.provider import Dependency

from .types import ConanPackageReference

###############################################################################
# Public API                                                                ###
###############################################################################

############################
### Conan Config Install ###
############################
def conan_config_install(conan_config_dir: Path) -> None:
    """Run "conan config install"."""
    run_command("conan", "config", "install", str(conan_config_dir))


##########################
### Conan Remote Login ###
##########################
def conan_remote_login(remote: str, user: str, password: str) -> None:
    """Run "conan remote login"."""
    run_command_assert_success(
        "conan",
        "remote",
        "login",
        remote,
        user,
        "-p",
        password,
    )

### Conan List
class ConanListResult(RootModel):
    root: Mapping[str, Mapping[ConanPackageReference, dict]]

def conan_list(remote: str, name: str) -> Mapping[ConanPackageReference, dict]:
    stdout, _ = run_command_assert_success(
        "conan",
        "list",
        "-f", "json",
        f"--remote={remote}",
        f"{name}/",
    )
    print(stdout)
    parsed_data = ConanListResult.model_validate_json(stdout)
    print(parsed_data)
    return parsed_data.root[remote]


###############################
### Conan Graph Build-Order ###
###############################
class ConanPackageInfo(BaseModel):
    settings: Mapping[str, str] | None = None

class ConanPackageAttributes(BaseModel):
    info: ConanPackageInfo

class ConanRecipeAttributes(BaseModel):
    ref: str
    depends: list[str]
    packages: list[list[ConanPackageAttributes]]

class ConanGraphBuildOrder(BaseModel):
    order: list[list[ConanRecipeAttributes]]

def conan_graph_buildorder(conanfile_path: Path, profile: str) -> ConanGraphBuildOrder:
    """Run "conan graph buildorder"."""
    stdout, _ = run_command_assert_success(
        "conan",
        "graph",
        "build-order",
        str(conanfile_path),
        "-pr:a", profile,
        "-f", "json",
        "--order-by", "recipe",
    )
    print(stdout)
    return ConanGraphBuildOrder.model_validate_json(stdout)


####################
### Conan Create ###
####################
def conan_create(package_dir: Path, profile: str) -> None:
    """Run "conan create"."""
    run_command_assert_success(
        "conan",
        "create",
        str(package_dir),
        "-pr:a", profile,
    )

####################
### Conan Upload ###
####################
def conan_upload(ref: ConanPackageReference, remote: str) -> None:
    """Run "conan upload"."""
    run_command_assert_success(
        "conan",
        "upload",
        "-r", remote,
        str(ref),
    )