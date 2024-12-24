# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


import os
from pathlib import Path
import tempfile
from cpp_dev.common.os import (
    is_valid_name,
    ensure_dir_exists,
    create_tmp_dir,
    updated_env,
)


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


def test_create_tmp_dir_without_base():
    with create_tmp_dir() as tmp_dir:
        assert tmp_dir.relative_to(tempfile.gettempdir())
        with create_tmp_dir() as tmp_dir2:
            assert tmp_dir != tmp_dir2


def test_create_tmp_dir_with_base(tmp_path: Path):
    with create_tmp_dir(tmp_path) as tmp_dir:
        assert tmp_dir.relative_to(tmp_dir)
        with create_tmp_dir(tmp_path) as tmp_dir2:
            assert tmp_dir != tmp_dir2


def test_create_tmp_dir_cleanup():
    with create_tmp_dir() as tmp_dir:
        assert tmp_dir.exists()
        created_tmp_dir = tmp_dir
    assert not created_tmp_dir.exists()


def test_updated_env_mod():
    ENV_VAR = "_TEST_0"
    INIT_VALUE = "0"
    MOD_VALUE = "1"
    os.environ[ENV_VAR] = INIT_VALUE
    with updated_env(**{ENV_VAR: MOD_VALUE}):
        assert os.environ[ENV_VAR] == MOD_VALUE
    assert os.environ[ENV_VAR] == INIT_VALUE
    del os.environ[ENV_VAR]


def test_updated_env_add():
    ENV_VAR = "_TEST_1"
    VALUE = "1"
    assert ENV_VAR not in os.environ
    with updated_env(**{ENV_VAR: VALUE}):
        assert os.environ[ENV_VAR] == VALUE
    assert ENV_VAR not in os.environ
