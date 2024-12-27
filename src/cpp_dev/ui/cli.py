# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import logging
import sys

import typed_argparse as tap

from cpp_dev.common.os import assert_supported_os

from .mgmt import InitArgs, command_init_cpd
from .project import (
    AddDependencyArgs,
    BuildArgs,
    CheckArgs,
    ExecutionArgs,
    FormatArgs,
    NewArgs,
    PackageArgs,
    TestArgs,
    command_add_dependency,
    command_build,
    command_check,
    command_execute,
    command_format,
    command_new,
    command_package,
    command_test,
)


def main() -> None:
    """Run main entry point for the cpd command line interface."""
    try:
        assert_supported_os()
        # assert_cpd_is_initialized(get_cpd_dir())  # noqa: ERA001

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
            ),
        ).bind(
            tap.Binding(NewArgs, command_new),
            tap.Binding(AddDependencyArgs, command_add_dependency),
            tap.Binding(BuildArgs, command_build),
            tap.Binding(ExecutionArgs, command_execute),
            tap.Binding(TestArgs, command_test),
            tap.Binding(CheckArgs, command_check),
            tap.Binding(FormatArgs, command_format),
            tap.Binding(PackageArgs, command_package),
            tap.Binding(InitArgs, command_init_cpd),
        ).run()
    except Exception:
        logging.exception("Failed to run cpd command")
        sys.exit(1)
