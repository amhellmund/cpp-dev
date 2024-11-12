# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
import typed_argparse as tap

from cpp_dev.tool.initialization import assert_cpd_is_initialized

from .project import (
    NewArgs,
    AddDependencyArgs,
    BuildArgs,
    ExecutionArgs,
    TestArgs,
    CheckArgs,
    FormatArgs,
    PackageArgs,
    command_new,
    command_format,
    command_add_dependency,
    command_build,
    command_check,
    command_execute,
    command_package,
    command_test,
)
from .mgmt import (
    InitArgs,
    command_init_cpd,
    UpdatePackageCacheArgs,
    command_update_package_cache,
    ListAvailablePackagesArgs,
    command_list_available_packages,
)


def main() -> None:
    assert_cpd_is_initialized()
    tap.Parser(
        tap.SubParserGroup(
            tap.SubParser("new", NewArgs, help="Create a new cpp-dev project"),
            tap.SubParser(
                "add-dep",
                AddDependencyArgs,
                help="Add a dependency to the project",
            ),
            tap.SubParser("build", BuildArgs, help="Build the project"),
            tap.SubParser("execute", ExecutionArgs, help="Execute the built code"),
            tap.SubParser("test", TestArgs, help="Run the tests"),
            tap.SubParser("check", CheckArgs, help="Perform static code analysis"),
            tap.SubParser("format", FormatArgs, help="Format the source code"),
            tap.SubParser(
                "package",
                PackageArgs,
                help="Package the project into a distributable cpp-dev format",
            ),
            tap.SubParser(
                "list-packages",
                ListAvailablePackagesArgs,
                help="List available packages for external dependencies",
            ),
            tap.SubParser(
                "mgmt",
                tap.SubParserGroup(
                    tap.SubParser(
                        "init",
                        InitArgs,
                        help="List available packages for external dependencies",
                    ),
                    tap.SubParser(
                        "update-package-cache",
                        UpdatePackageCacheArgs,
                        help="Update the local package cache with external dependencies",
                    ),
                ),
                help="Commands to manage cpd on the local machine",
            ),
        )
    ).bind(
        tap.Binding(NewArgs, command_new),
        tap.Binding(AddDependencyArgs, command_add_dependency),
        tap.Binding(BuildArgs, command_build),
        tap.Binding(ExecutionArgs, command_execute),
        tap.Binding(TestArgs, command_test),
        tap.Binding(CheckArgs, command_check),
        tap.Binding(FormatArgs, command_format),
        tap.Binding(PackageArgs, command_package),
        tap.Binding(ListAvailablePackagesArgs, command_list_available_packages),
        tap.Binding(InitArgs, command_init_cpd),
        tap.Binding(UpdatePackageCacheArgs, command_update_package_cache),
    ).run()
