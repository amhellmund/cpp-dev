# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path

from cpp_dev.common.version import SemanticVersion
from cpp_dev.tool.version import read_version_file, write_version_file


def test_version_file_roundtrip(tmp_path: Path) -> None:
    expected_version = SemanticVersion("1.2.3")
    write_version_file(tmp_path, expected_version)
    version = read_version_file(tmp_path)

    assert expected_version == version
