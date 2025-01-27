# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
import re
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

class ConanCommandException(Exception):
    """Exception for raising issues during Conan command execution."""
    def __init__(self, command: str, msg: str) -> None:
        self._command = command
        self._msg = msg
        super().__init__(f"{self._command} failed: {self._msg}")


ConanSetting = Literal["compiler", "compiler.cppstd"]


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
    parsed_data = ConanListResult.model_validate_json(stdout)
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


COMMAND_GRAPH_BUILDORDER = "graph-buildorder"

def _handle_package_resolution_error(stderr: str) -> None:
    regex_unable_to_find = re.compile(r"Unable to find '([^']+)'")
    match = regex_unable_to_find.search(stderr)
    if match:
        raise ConanCommandException(
            command=COMMAND_GRAPH_BUILDORDER,
            msg=f"unable to find package '{match.group(1)}'",
        )
    
def _handle_package_version_conflict(stderr: str) -> None:
    regex_version_conflict = re.compile(r"Version conflict: Conflict between ([^ ]+) and ([^ ]+) in the graph")
    match = regex_version_conflict.search(stderr)
    if match:
        raise ConanCommandException(
            command=COMMAND_GRAPH_BUILDORDER,
            msg=f"version conflict between '{match.group(1)}' and '{match.group(2)}'",
        )

def _handle_graph_buildorder_error(stderr: str) -> None:
    _handle_package_resolution_error(stderr)
    _handle_package_version_conflict(stderr)

    raise ConanCommandException(
        command=COMMAND_GRAPH_BUILDORDER,
        msg="generic error",
    )

def conan_graph_buildorder(conanfile_path: Path, profile: str, settings: dict[ConanSetting, object]) -> ConanGraphBuildOrder:
    """Run "conan graph buildorder"."""
    command = [
        "conan",
        "graph",
        "build-order",
        str(conanfile_path),
        "-pr:a", profile,
        "-f", "json",
        "--order-by", "recipe",
    ]
    for key, value in settings.items():
        command.extend(["-s:a", f"{key}={value}"])
    rc, stdout, stderr = run_command(
        *command
    )
    if rc != 0:
        print(f"STDOUT: {stderr}")
        _handle_graph_buildorder_error(stderr)

    return ConanGraphBuildOrder.model_validate_json(stdout)


####################
### Conan Create ###
####################

def conan_create(package_dir: Path, profile: str, settings: dict[ConanSetting, object]) -> None:
    """Run "conan create"."""
    command = [
        "conan",
        "create",
        str(package_dir),
        "-pr:a", profile,
    ]
    for key, value in settings.items():
        command.extend(["-s:a", f"{key}={value}"])
    run_command_assert_success(
        *command
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