# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
from unittest.mock import patch

import pytest

from cpp_dev.tool.init import assert_cpd_is_initialized, initialize_cpd


def test_initialize_cpd(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError):
        assert_cpd_is_initialized(tmp_path)

    with patch("cpp_dev.conan.commands._set_conan_default_user_and_password", return_value=None) as mock:
        initialize_cpd(tmp_path)
        mock.assert_called_once()

    assert (tmp_path / ".cpd").exists()
    version_file = tmp_path / ".cpd" / "version.txt"
    assert version_file.exists()
    assert version_file.read_bytes() == b"0.0.0"
    assert (tmp_path / ".cpd" / "conan2").exists()
    assert (tmp_path / ".cpd" / "conan2" / "settings.yml").exists()

    assert_cpd_is_initialized(tmp_path)
