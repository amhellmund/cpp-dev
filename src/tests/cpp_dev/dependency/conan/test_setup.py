# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
from unittest.mock import patch

from cpp_dev.dependency.conan.setup import (get_conan_config_source_dir,
                                            initialize_conan)


def test_initialize_conan(tmp_path: Path) -> None:
    with patch("cpp_dev.dependency.conan.setup.conan_remote_login") as mock:
        initialize_conan(tmp_path, get_conan_config_source_dir())
        mock.assert_called_once()

    assert (tmp_path / "remotes.json").exists()
    assert (tmp_path / "settings.yml").exists()
    assert (tmp_path / "profiles" / "ubuntu-24.04-x86_64").exists()
