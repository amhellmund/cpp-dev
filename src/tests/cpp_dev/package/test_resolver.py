# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

import pytest

from pytest_httpserver import HTTPServer
from pathlib import Path
from cpp_dev.common.types import OperatingSystemDistribution, SemanticVersion
from cpp_dev.package.resolver import PackageResolverLocal, PackageResolverRemote
from cpp_dev.package.types import PackageIndex


@pytest.fixture()
def simple_repo_path() -> Path:
    return Path(__file__).parent / "data" / "simple"


def _assert_simple_package_index(index: PackageIndex) -> None:
    assert index.repository == "repo"
    assert len(index.packages) == 1

    package = index.packages[0]
    assert package.name == "simple_package"
    assert package.latest == SemanticVersion("1.0.0")
    assert len(package.versions) == 1

    assert SemanticVersion("1.0.0") in package.versions
    version = package.versions[SemanticVersion("1.0.0")]
    assert version.dependencies == []
    assert version.path == "repo-simple_package-1.0.0.txt"


def test_package_resolver_local_for_index(simple_repo_path: Path):
    resolver = PackageResolverLocal(
        simple_repo_path,
        OperatingSystemDistribution(name="os", version="version"),
    )
    index = resolver.get_index("repo")
    _assert_simple_package_index(index)


def test_package_resolver_local_for_file(simple_repo_path: Path):
    resolver = PackageResolverLocal(
        simple_repo_path,
        OperatingSystemDistribution(name="os", version="version"),
    )

    package_data = resolver.get_package_file("repo-simple_package-1.0.0.txt")
    assert package_data == b"package-content"


@pytest.fixture
def http_file_server(httpserver: HTTPServer, simple_repo_path: Path) -> HTTPServer:
    files = [file for file in simple_repo_path.glob("**/*") if file.is_file()]
    for file in files:
        rel_path = file.relative_to(simple_repo_path)
        httpserver.expect_request(f"/{rel_path}").respond_with_data(file.read_bytes())
    return httpserver


def test_apckage_resolver_remote_for_index(http_file_server: HTTPServer):
    resolver = PackageResolverRemote(
        http_file_server.url_for("/"),
        OperatingSystemDistribution(name="os", version="version"),
    )
    index = resolver.get_index("repo")
    _assert_simple_package_index(index)


def test_package_resolver_remote_for_file(http_file_server: HTTPServer):
    resolver = PackageResolverRemote(
        http_file_server.url_for("/"),
        OperatingSystemDistribution(name="os", version="version"),
    )

    package_data = resolver.get_package_file("repo-simple_package-1.0.0.txt")
    assert package_data == b"package-content"
