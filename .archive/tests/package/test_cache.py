# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
import pytest

from cpp_dev.common.file_io import FileIOLocal
from cpp_dev.package.cache import PackageCache
from cpp_dev.package.store import PackageStore
from cpp_dev.package.types import OperatingSystem, PackageRef


@pytest.fixture
def test_os():
    return OperatingSystem(
        arch="x86_64",
        name="os",
        version="version",
    )


@pytest.fixture()
def package_store(test_os: OperatingSystem) -> PackageStore:
    return PackageStore(
        file_io=FileIOLocal(Path(__file__).parent / "data"),
        os=test_os,
    )


@pytest.fixture()
def package_cache(package_store: PackageStore, tmp_path: Path) -> PackageCache:
    cache_dir = tmp_path / "cache"
    return PackageCache(package_store, cache_dir=cache_dir)


def test_cache_update_repositories(package_cache: PackageCache):
    package_cache.update_repositories()

    assert (package_cache.cache_dir / "indexes" / "repo.json").exists()


@pytest.mark.parametrize(
    "package_ref",
    [
        PackageRef("repo-nosimple_package-1.0.0"),
        PackageRef("norepo-simple_package-1.0.0"),
        PackageRef("repo-simple_package-1.0.1"),
    ],
)
def test_cache_get_package_does_not_exist(
    package_cache: PackageCache, package_ref: PackageRef
):
    with pytest.raises(ValueError):
        package_cache.get_package_with_dependencies(package_ref)


def test_cache_get_package(package_cache: PackageCache):
    package_cache.update_repositories()
    cached_packages = package_cache.get_package_with_dependencies(
        PackageRef("repo-simple_package-1.0.0")
    )

    assert len(cached_packages) == 1
