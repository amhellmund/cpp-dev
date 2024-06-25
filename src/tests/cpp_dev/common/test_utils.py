# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
import tempfile
from cpp_dev.common.utils import is_valid_name, ensure_dir_exists, create_tmp_dir


def test_is_valid_name():
    assert is_valid_name("test")
    assert is_valid_name("te_st")
    assert is_valid_name("test_")

    assert not is_valid_name("_test")
    assert not is_valid_name("teST")
    assert not is_valid_name("te12_A")


def test_ensure_dir_exists(tmp_path: Path):
    target_dir = tmp_path / "new_dir"
    assert not target_dir.exists()
    ensure_dir_exists(target_dir)
    assert target_dir.exists()


def test_create_tmp_dir_without_base(tmp_path: Path):
    with create_tmp_dir() as tmp_dir:
        assert tmp_dir.relative_to(tempfile.gettempdir())
        with create_tmp_dir() as tmp_dir2:
            assert tmp_dir != tmp_dir2


def teste_create_tmp_dir_with_base(tmp_path: Path):
    with create_tmp_dir(tmp_path) as tmp_dir:
        assert tmp_dir.relative_to(tmp_dir)
        with create_tmp_dir(tmp_path) as tmp_dir2:
            assert tmp_dir != tmp_dir2
