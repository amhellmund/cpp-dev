# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import pytest

from cpp_dev.common.process import run_command, run_command_assert_success


def test_run_command() -> None:
    return_code, stdout, stderr = run_command("echo", "cpd")
    assert return_code == 0
    assert stdout == "cpd"
    assert stderr == ""


def test_run_command_assert_success_no_failure() -> None:
    stdout, stderr = run_command_assert_success("echo", "cpd")
    assert stdout == "cpd"
    assert stderr == ""


def test_run_command_assert_success_failure() -> None:
    with pytest.raises(RuntimeError):
        run_command_assert_success("false")
