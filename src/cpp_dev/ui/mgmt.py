# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import typed_argparse as tap


class InitArgs(tap.TypedArgs):
    pass


class ListAvailablePackagesArgs(tap.TypedArgs):
    pass


class UpdatePackageCacheArgs(tap.TypedArgs):
    pass


def command_init_cpd(args: InitArgs) -> None:
    pass


def command_update_package_cache(args: UpdatePackageCacheArgs) -> None:
    pass


def command_list_available_packages(args: ListAvailablePackagesArgs) -> None:
    pass
