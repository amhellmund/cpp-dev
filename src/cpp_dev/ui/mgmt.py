# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import typed_argparse as tap

from cpp_dev.tool.version import get_cpd_version_from_code


class VersionArgs(tap.TypedArgs):
    """Arguments for the 'cpd version' command."""


def command_version(_: VersionArgs) -> None:
    """Print the version of the cpd command."""
    print(f"cpp-dev version {get_cpd_version_from_code()}")  # noqa: T201
