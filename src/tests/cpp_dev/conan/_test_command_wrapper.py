# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import json
from unittest.mock import patch

from cpp_dev.conan.command_wrapper import (conan_create,
                                           conan_graph_buildorder, conan_list,
                                           conan_remote_login)


def test_conan_list() -> None:
    with patch("cpp_dev.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        mock_run_command.return_value = (json.dumps({"official": {}}), None)
        conan_list("official", "cpd")
        mock_run_command.assert_called_once_with(
            "conan",
            "list",
            "-f", "json",
            "--remote=official",
            "cpd/",
        )

def test_conan_remote_login() -> None:
    with patch("cpp_dev.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        conan_remote_login("official", "user", "password")
        mock_run_command.assert_called_once_with(
            "conan",
            "remote",
            "login",
            "official",
            "user",
            "-p",
            "password",
        )

def test_conan_graph_buildorder() -> None:
    with patch("cpp_dev.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        mock_run_command.return_value = (json.dumps({}), None)
        conan_graph_buildorder("conanfile.txt", "profile")
        mock_run_command.assert_called_once_with(
            "conan",
            "graph",
            "buildorder",
            "conanfile.txt",
            "-pr:a",
            "profile",
            "-f", "json",
            "--order-by",
            "recipe",
        )

def test_conan_create() -> None:
    with patch("cpp_dev.conan.command_wrapper.run_command_assert_success") as mock_run_command:
        conan_create(Path("package_dir"), "profile")
        mock_run_command.assert_called_once_with(
            "conan",
            "graph",
            "buildorder",
            "conanfile.txt",
            "-pr:a",
            "profile",
            "-f", "json",
            "--order-by",
            "recipe",
        )