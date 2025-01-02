# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import patch

import pytest

from cpp_dev.common.os_detection import OperatingSystemType, assert_supported_os, detect_os


@contextmanager
def patch_os_detection_module(os_id: str, os_version: str) -> Generator[None]:
    with (
        patch("cpp_dev.common.os_detection.distro.id", return_value=os_id),
        patch("cpp_dev.common.os_detection.distro.version", return_value=os_version),
    ):
        yield


@pytest.mark.parametrize(
    ("os_id", "os_version", "expected_os_type"),
    [
        ("ubuntu", "24.04", OperatingSystemType.Ubuntu2404),
        ("centos", "0", OperatingSystemType.Unsupported),
    ],
)
def test_detect_os(os_id: str, os_version: str, expected_os_type: OperatingSystemType) -> None:
    with patch_os_detection_module(os_id, os_version):
        operating_system = detect_os()
        assert operating_system.type == expected_os_type


@pytest.mark.parametrize(
    ("os_id", "os_version"),
    [("ubuntu", "24.04")],
)
def test_assert_supported_os_ok(os_id: str, os_version: str) -> None:
    with patch_os_detection_module(os_id, os_version):
        assert_supported_os()


@pytest.mark.parametrize(
    ("os_id", "os_version"),
    [("centos", "7")],
)
def test_assert_supported_os_not_ok(os_id: str, os_version: str) -> None:
    with (
        patch_os_detection_module(os_id, os_version),
        pytest.raises(RuntimeError, match="Unsupported operating system"),
    ):
        assert_supported_os()
