# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from dataclasses import dataclass
from cpp_dev.package.store import PackageStore


@dataclass
class TransitivePackageInfo:
    


class PackageCache:
    def __init__(self, package_store: PackageStore) -> None:
        self._package_store = package_store

    def add_package(self, package_ref: str) -> None: ...
