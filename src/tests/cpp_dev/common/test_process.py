# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from cpp_dev.common.process import run_command


def test_run_command() -> None:
    """Test the run_command function."""
    stdout, stderr = run_command("echo", "cpd")
    assert stdout == "cpd"
    assert stderr == ""
