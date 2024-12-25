# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from unittest.mock import patch

import pytest

from cpp_dev.common.os import OperatingSystemType, assert_supported_os, detect_os


@pytest.mark.parametrize(
    ("os_data", "expected_os_type"),
    [
        (("ubuntu", "24.04"), OperatingSystemType.Ubuntu2404),
        (("centos", "0"), OperatingSystemType.Unsupported),
    ],
)
def test_detect_os(os_data: tuple[str, str], expected_os_type: OperatingSystemType) -> None:
    os_id, os_version = os_data
    with (
        patch("cpp_dev.common.os.distro.id", return_value=os_id),
        patch("cpp_dev.common.os.distro.version", return_value=os_version),
    ):
        operating_system = detect_os()
        assert operating_system.type == expected_os_type


@pytest.mark.parametrize(
    ("os_data"),
    [("ubuntu", "24.04")],
)
def test_assert_supported_os_ok(os_data: tuple[str, str]) -> None:
    os_id, os_version = os_data
    with (
        patch("cpp_dev.common.os.distro.id", return_value=os_id),
        patch("cpp_dev.common.os.distro.version", return_value=os_version),
    ):
        assert_supported_os()


@pytest.mark.parametrize(
    ("os_data"),
    [("centos", "7")],
)
def test_assert_supported_os_not_ok(os_data: tuple[str, str]) -> None:
    os_id, os_version = os_data
    with (
        patch("cpp_dev.common.os.distro.id", return_value=os_id),
        patch("cpp_dev.common.os.distro.version", return_value=os_version),
        pytest.raises(RuntimeError),
    ):
        assert_supported_os()
