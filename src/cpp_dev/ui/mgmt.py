# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import typed_argparse as tap


class InitArgs(tap.TypedArgs):
    """Arguments for the 'cpd init' command."""


def command_init_cpd(args: InitArgs) -> None:
    """Initialize a new C++ project."""
