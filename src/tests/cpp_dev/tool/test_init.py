# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
from pytest import raises

from cpp_dev.tool.init import assert_cpd_is_initialized, initialize_cpd


def test_initialize_cpd(tmp_path: Path) -> None:
    with raises(RuntimeError):
        assert_cpd_is_initialized(tmp_path)

    initialize_cpd(tmp_path)

    assert (tmp_path / ".cpd").exists()
    assert (tmp_path / ".cpd" / "conan2").exists()
    assert (tmp_path / ".cpd" / "conan2" / "settings.yml").exists()

    assert_cpd_is_initialized(tmp_path)
