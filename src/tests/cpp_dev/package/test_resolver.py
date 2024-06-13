# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from contextlib import contextmanager
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from cpp_dev.common.types import OperatingSystemDistribution, SemanticVersion
from cpp_dev.package.resolver import PackageResolverLocal


def _get_repo_dir(name: str) -> Path:
    return Path(__file__).parent / "data" / name


def test_package_resolver_local_for_index():
    resolver = PackageResolverLocal(
        _get_repo_dir("simple"),
        OperatingSystemDistribution(name="os", version="version"),
    )

    index = resolver.get_index("repo")
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


def test_package_resolver_local_for_file():
    resolver = PackageResolverLocal(
        _get_repo_dir("simple"),
        OperatingSystemDistribution(name="os", version="version"),
    )

    package_data = resolver.get_package_file("repo-sample_package-1.0.0.txt")
    assert package_data == b"package-content"


# @contextmanager
# def http_server(port: int):
#     httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
#     try:
#         yield HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
#     finally:
#         thing.close()


# def test_apckage_resolver_remote_for_index():
#     httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
#     httpd.
