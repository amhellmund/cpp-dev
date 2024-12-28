# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from argparse import ArgumentTypeError
from pathlib import Path

import typed_argparse as tap

from cpp_dev.common.types import CppStandard
from cpp_dev.common.utils import is_valid_name
from cpp_dev.project.setup import setup_project
from cpp_dev.project.types import ProjectConfig, SemanticVersion

###############################################################################
# Public API                                                                ###
###############################################################################


def _validate_project_name(name: str) -> str:
    if not is_valid_name(name):
        raise ArgumentTypeError(f"Invalid package name: got {name}, expected characters, underscores only.")
    return name


class NewProjectArgs(tap.TypedArgs):
    """Arguments for the 'cpd new' command."""

    name: str = tap.arg(help="The name of the project.", positional=True, type=_validate_project_name)
    version: SemanticVersion = tap.arg(help="The version of the project.")
    std: CppStandard = tap.arg(help="The C++ standard to use for the project.", default="c++20")
    parent_dir: Path = tap.arg(
        default=Path.cwd(),
        help="The parent directory to create the project directory into. "
        "The current directory is used if this option is not provided. ",
    )
    author: str | None = tap.arg(help="The author of the project.")
    license: str | None = tap.arg(help="The license of the project.")
    description: str | None = tap.arg(help="A short description of the project.")


class AddDependencyArgs(tap.TypedArgs):
    """Arguments for the 'cpd add' command."""

    dependency_spec: list[str] = tap.arg(
        help="""The dependency to add to the project. The format is '<user>/<name>[<version_spec>]'.
        The parameter <user> is the user or organization that owns the dependency.
        This parameter is optional in which case an 'official' dependency is assumed.
        The parameter <name> is the name of the dependency.
        The parameter <version_spec> supports an exact version, lower/upper bounds, intervals or 'latest'.
        This parameter is optional in which case the latest version is used.
        The exact version is specified as '<major>.<minor>.<patch>', while lower/upper bounds and intervals
        use the format '< | <= | > | >= <major>[.<minor>[.<patch>]]' with minor and parts parts being optional.
        Multiple range specs can be combined with ',' forming a logical AND conjunction.
        Examples: boost, boost[latest], boost[1.0.0], boost[>=1.0], boost[<2.0], official/boost[>=1.5,<2.0]
        """,
        positional=True,
    )


class BuildArgs(tap.TypedArgs):
    """Arguments for the 'cpd build' command."""


class ExecutionArgs(tap.TypedArgs):
    """Arguments for the 'cpd execute' command."""


class TestArgs(tap.TypedArgs):
    """Arguments for the 'cpd test' command."""


class CheckArgs(tap.TypedArgs):
    """Arguments for the 'cpd check' command."""


class FormatArgs(tap.TypedArgs):
    """Arguments for the 'cpd format' command."""


class PackageArgs(tap.TypedArgs):
    """Arguments for the 'cpd package' command."""


def command_new_project(args: NewProjectArgs) -> None:
    """Create a new project with the specified configuration."""
    setup_project(
        project_config=ProjectConfig(
            name=args.name,
            version=args.version,
            std=args.std,
            author=args.author,
            license=args.license,
            description=args.description,
            dependencies=[],
            dev_dependencies=[],
            cpd_dependencies=[],
        ),
    )


def command_add_dependency(args: AddDependencyArgs) -> None:
    """Add a new dependency to the project."""


def command_build(args: BuildArgs) -> None:
    """Build the project."""


def command_execute(args: ExecutionArgs) -> None:
    """Execute the the binary in the project."""


def command_test(args: TestArgs) -> None:
    """Run the tests for the project."""


def command_check(args: CheckArgs) -> None:
    """Run the SCA checks for the project."""


def command_format(args: FormatArgs) -> None:
    """Format the source code of the project."""


def command_package(args: PackageArgs) -> None:
    """Package the project."""


###############################################################################
# Implementation                                                            ###
###############################################################################
