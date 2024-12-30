# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from cpp_dev.conan.config import get_conan_config_source_dir, get_remotes


def test_get_remotes() -> None:
    conan_remotes = get_remotes(get_conan_config_source_dir())

    assert len(conan_remotes.remotes) == 1
    conan_remotes.remotes[0].name == "cpd"
