from .arg_types import (
    NewArgs,
    AddDependencyArgs,
    BuildArgs,
    ExecutionArgs,
    TestArgs,
    CheckArgs,
    FormatArgs,
    PackageArgs,
    ListAvailablePackagesArgs
)

def command_new(args: NewArgs) -> None:
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