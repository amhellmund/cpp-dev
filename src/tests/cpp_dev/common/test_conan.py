# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

from cpp_dev.common.conan import initialize_conan


def test_initialize_conan(tmp_path: Path) -> None:
    initialize_conan(tmp_path)

    assert (tmp_path / "remotes.json").exists()
    assert (tmp_path / "settings.yml").exists()
    assert (tmp_path / "config" / "profiles" / "ubuntu2404_dev_tooling").exists()
