# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from argparse import ArgumentTypeError
from typing import Optional
import typed_argparse as tap

from cpp_dev.common.types import CppStandard
from cpp_dev.common.utils import is_valid_name
from cpp_dev.project.types import SemanticVersion


def _validate_project_name(name: str) -> str:
    if not is_valid_name(name):
        raise ArgumentTypeError(
            f"Invalid package name: got {name}, expected characters, underscores only."
        )
    return name


class NewArgs(tap.TypedArgs):
    std: CppStandard = tap.arg(
        help="The C++ standard to use for the project.", default="c++20"
    )
    name: str = tap.arg(
        help="The name of the project.", positional=True, type=_validate_project_name
    )
    version: SemanticVersion = tap.arg(help="The version of the project.")
    author: Optional[str] = tap.arg(help="The author of the project.")
    license: Optional[str] = tap.arg(help="The license of the project.")
    description: Optional[str] = tap.arg(help="A short description of the project.")


class AddDependencyArgs(tap.TypedArgs):
    pass


class BuildArgs(tap.TypedArgs):
    pass


class ExecutionArgs(tap.TypedArgs):
    pass


class TestArgs(tap.TypedArgs):
    pass


class CheckArgs(tap.TypedArgs):
    pass


class FormatArgs(tap.TypedArgs):
    pass


class PackageArgs(tap.TypedArgs):
    pass


class ListAvailablePackagesArgs(tap.TypedArgs):
    pass
