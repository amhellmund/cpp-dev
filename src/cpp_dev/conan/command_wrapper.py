# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, RootModel

from cpp_dev.common.process import run_command, run_command_assert_success

from .types import ConanPackageReference

###############################################################################
# Public API                                                                ###
###############################################################################


def conan_config_install(conan_config_dir: Path) -> None:
    """Run 'conan config install'."""
    run_command("conan", "config", "install", str(conan_config_dir))


def conan_remote_login(remote: str, user: str, password: str) -> None:
    """Run 'conan remote login'."""
    run_command_assert_success(
        "conan",
        "remote",
        "login",
        remote,
        user,
        "-p",
        password,
    )

class ConanRemoteListResult(RootModel):
    root: Mapping[str, Mapping[str, dict]]

def conan_list(remote: str, name: str) -> Mapping[ConanPackageReference, dict]:
    stdout, _ = run_command_assert_success(
        "conan",
        "list",
        "--json",
        f"--remote={remote}",
        f"{name}/",
    )
    return json.loads(stdout)[remote]

def conan_graph_buildorder(conanfile_path: Path, profile: str) -> list[str]:
    stdout, _ = run_command_assert_success(
        "conan",
        "graph",
        "buildorder",
        str(conanfile_path),
        "-pr:a", profile,
        "--json",
        "--order-by", "recipe",
    )