import typed_argparse as tap

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
from .commands import (
    command_new,
    command_add_dependency,
    command_build,
    command_execute,
    command_test,
    command_check,
    command_format,
    command_package,
    command_list_available_packages,
)


def main () -> None:
    tap.Parser(
        tap.SubParserGroup(
            tap.SubParser("new", NewArgs, help="Create a new cpp-dev project"),
            tap.SubParser("add-dep", AddDependencyArgs, help="Add a dependency to the project"),
            tap.SubParser("build", CheckArgs, help="Build the project"),
            tap.SubParser("execute", ExecutionArgs, help="Execute the built code"),
            tap.SubParser("test", BuildArgs, help="Run the tests"),
            tap.SubParser("check", CheckArgs, help="Perform static code analysis"),
            tap.SubParser("format", FormatArgs, help="Format the source code"),
            tap.SubParser("package", PackageArgs, help="Package the project into a distributable cpp-dev format"),
            tap.SubParser("list-packages", ListAvailablePackagesArgs, help="List available packages for external dependencies"),
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
    ).run()