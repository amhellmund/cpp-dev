# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from cpp_dev.common.utils import updated_env

###############################################################################
# Public API                                                                ###
###############################################################################

CONAN_HOME_ENV_VAR = "CONAN_HOME"


@contextmanager
def conan_env(conan_home: Path) -> Generator[None]:
    """A context manager for setting the CONAN_HOME environment variable."""
    with updated_env(**{CONAN_HOME_ENV_VAR: str(conan_home)}):
        yield