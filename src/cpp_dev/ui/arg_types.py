# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from argparse import ArgumentTypeError
from typing import Optional
import typed_argparse as tap

from cpp_dev.common.types import CppStandard, SemanticVersion

def _validate_semantic_version(version: str) -> SemanticVersion:
    try:
        return SemanticVersion.from_string(version)
    except ValueError as e:
        raise ArgumentTypeError(str(e))

class NewArgs(tap.TypedArgs):
    std: CppStandard = tap.arg(help="The C++ standard to use for the project.", default="20")
    name: str = tap.arg(help="The name of the project.", positional=True)
    version: SemanticVersion = tap.arg(help="The version of the project.", type=_validate_semantic_version)
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