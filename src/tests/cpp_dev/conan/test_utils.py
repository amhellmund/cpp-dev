# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import os

from cpp_dev.conan.utils import CONAN_HOME_ENV_VAR, conan_env


def test_conan_env() -> None:
    if CONAN_HOME_ENV_VAR in os.environ:
        del os.environ[CONAN_HOME_ENV_VAR]
    with conan_env("conan"):
        assert CONAN_HOME_ENV_VAR in os.environ
        assert os.environ[CONAN_HOME_ENV_VAR] == "conan"
    assert CONAN_HOME_ENV_VAR not in os.environ