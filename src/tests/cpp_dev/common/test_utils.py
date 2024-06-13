# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License


from cpp_dev.common.utils import is_valid_name


def test_is_valid_name():
    assert is_valid_name("test")
    assert is_valid_name("te_st")
    assert is_valid_name("test_")

    assert not is_valid_name("_test")
    assert not is_valid_name("teST")
    assert not is_valid_name("te12_A")
