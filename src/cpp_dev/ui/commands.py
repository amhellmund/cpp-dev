# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from cpp_dev.project.setup import setup_project

from .arg_types import (
    NewArgs,
    AddDependencyArgs,
    BuildArgs,
    ExecutionArgs,
    TestArgs,
    CheckArgs,
    FormatArgs,
    PackageArgs,
    ListAvailablePackagesArgs,
)


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


def command_list_available_packages(args: ListAvailablePackagesArgs) -> None:
    pass
