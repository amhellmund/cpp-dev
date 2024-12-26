# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import logging
import subprocess

###############################################################################
# Public API                                                                ###
###############################################################################


def run_command(command: str, *args: str) -> tuple[str, str]:
    """Run a command with the specified arguments.

    This function blocks until the command has finished.
    """
    logging.debug(f"Running command: {command} {args}")
    result = subprocess.run([command, *args], check=True, capture_output=True)  # noqa: S603

    logging.debug(f"Command return code: {result.returncode}")

    stdout = result.stdout.decode("utf-8").strip()
    logging.debug(f"Command output: {stdout}")

    stderr = result.stderr.decode("utf-8").strip()
    logging.debug(f"Command error output: {stderr}")
    if result.returncode != 0:
        raise RuntimeError(f"Failed to run command: {command} {args}")

    return stdout, stderr
