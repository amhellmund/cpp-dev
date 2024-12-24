# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import subprocess


def run_command(command: str, *args: str) -> None:
    """
    Run a command with the specified arguments.

    This function blocks until the command has finished.
    """
    return subprocess.run([command, *args], check=True, capture_output=True)
