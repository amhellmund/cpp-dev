# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import os
import tempfile
from pathlib import Path

from cpp_dev.common.utils import (
    create_tmp_dir,
    ensure_dir_exists,
    is_valid_name,
    updated_env,
)


def test_is_valid_name() -> None:
    assert is_valid_name("test")
    assert is_valid_name("te_st")
    assert is_valid_name("test_")

    assert not is_valid_name("_test")
    assert not is_valid_name("teST")
    assert not is_valid_name("te12_A")


def test_ensure_dir_exists(tmp_path: Path) -> None:
    target_dir = tmp_path / "new_dir"
    assert not target_dir.exists()
    ensure_dir_exists(target_dir)
    assert target_dir.exists()


def test_create_tmp_dir_without_base() -> None:
    with create_tmp_dir() as tmp_dir:
        assert tmp_dir.relative_to(tempfile.gettempdir())
        with create_tmp_dir() as tmp_dir2:
            assert tmp_dir != tmp_dir2


def test_create_tmp_dir_with_base(tmp_path: Path) -> None:
    with create_tmp_dir(tmp_path) as tmp_dir:
        assert tmp_dir.relative_to(tmp_dir)
        with create_tmp_dir(tmp_path) as tmp_dir2:
            assert tmp_dir != tmp_dir2


def test_create_tmp_dir_cleanup() -> None:
    with create_tmp_dir() as tmp_dir:
        assert tmp_dir.exists()
        created_tmp_dir = tmp_dir
    assert not created_tmp_dir.exists()


def test_updated_env_mod() -> None:
    env_var = "_TEST_0"
    init_value = "0"
    mod_value = "1"
    os.environ[env_var] = init_value
    with updated_env(**{env_var: mod_value}):
        assert os.environ[env_var] == mod_value
    assert os.environ[env_var] == init_value
    del os.environ[env_var]


def test_updated_env_add() -> None:
    env_var = "_TEST_1"
    value = "1"
    assert env_var not in os.environ
    with updated_env(**{env_var: value}):
        assert os.environ[env_var] == value
    assert env_var not in os.environ
