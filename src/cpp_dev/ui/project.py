# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from argparse import ArgumentTypeError
from pathlib import Path
from typing import Optional
import typed_argparse as tap

from cpp_dev.common.types import CppStandard
from cpp_dev.common.utils import is_valid_name
from cpp_dev.project.setup import setup_project
from cpp_dev.project.types import SemanticVersion


def _validate_project_name(name: str) -> str:
    if not is_valid_name(name):
        raise ArgumentTypeError(
            f"Invalid package name: got {name}, expected characters, underscores only."
        )
    return name


class NewArgs(tap.TypedArgs):
    name: str = tap.arg(
        help="The name of the project.", positional=True, type=_validate_project_name
    )
    version: SemanticVersion = tap.arg(help="The version of the project.")
    std: CppStandard = tap.arg(
        help="The C++ standard to use for the project.", default="c++20"
    )
    parent_dir: Path = tap.arg(
        default=Path.cwd(),
        help="The parent directory to create the project directory into. "
        "The current directory is used if this option is not provided. ",
    )
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


def command_new(args: NewArgs) -> None:
    setup_project(
        name=args.name,
        version=args.version,
        std=args.std,
        parent_dir=args.parent_dir,
        author=args.author,
        license=args.license,
        description=args.description,
    )
    pass


def command_add_dependency(args: AddDependencyArgs) -> None:
    pass


def command_build(args: BuildArgs) -> None:
    pass


def command_execute(args: ExecutionArgs) -> None:
    pass


def command_test(args: TestArgs) -> None:
    pass


def command_check(args: CheckArgs) -> None:
    pass


def command_format(args: FormatArgs) -> None:
    pass


def command_package(args: PackageArgs) -> None:
    pass
