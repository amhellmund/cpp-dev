# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
import pytest

from cpp_dev.common.file_io import FileIOLocal
from cpp_dev.package.cache import PackageCache
from cpp_dev.package.store import PackageStore
from cpp_dev.package.types import OperatingSystem


@pytest.fixture
def test_os():
    return OperatingSystem(
        arch="x86_64",
        name="os",
        version="version",
    )


@pytest.fixture()
def package_store(test_os) -> PackageStore:
    return PackageStore(
        file_io=FileIOLocal(Path(__file__).parent / "data"),
        os=test_os,
    )


def test_cache_update_repositories(package_store: PackageStore, tmp_path: Path):
    cache_dir = tmp_path / "cache"
    cache = PackageCache(package_store, cache_dir=cache_dir)
    cache.update_repositories()

    assert (cache_dir / "indexes" / "repo.json").exists()
