# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path
from unittest.mock import patch

import pytest

from cpp_dev.common.utils import updated_env
from cpp_dev.common.version import SemanticVersion
from cpp_dev.tool.init import assure_cpd_is_initialized, get_conan_home_dir, get_cpd_dir, initialize_cpd, update_cpd
from cpp_dev.tool.version import get_cpd_version_from_code, write_version_file


@pytest.fixture(autouse=True)
def conan_remote_login() -> object:
    """Mock the conan user and password setting function."""
    with patch("cpp_dev.conan.setup.conan_remote_login", return_value=None) as mock:
        yield mock


@pytest.fixture
def cpd_dir(tmp_path: Path) -> Path:
    return get_cpd_dir(tmp_path)


def test_get_cpd_dir(tmp_path: Path) -> None:
    assert get_cpd_dir() == get_cpd_dir(Path.home())
    assert get_cpd_dir(tmp_path) == get_cpd_dir(tmp_path)

    cpd_env_dir = tmp_path / "cpd-env-dir"
    with updated_env(CPD_HOME=cpd_env_dir):
        assert get_cpd_dir() == get_cpd_dir(cpd_env_dir)


def test_assure_cpd_is_initialized(cpd_dir: Path) -> None:
    assert not cpd_dir.exists()
    assure_cpd_is_initialized(cpd_dir)
    assert cpd_dir.exists()


def test_initialize_cpd(cpd_dir: Path) -> None:
    initialize_cpd(cpd_dir)

    assert cpd_dir.exists()
    version_file = cpd_dir / "version.txt"
    assert version_file.exists()
    assert version_file.read_text() == str(get_cpd_version_from_code())

    conan_dir = get_conan_home_dir(cpd_dir)
    assert conan_dir.exists()
    assert (conan_dir / "settings.yml").exists()
    assert (conan_dir / "settings.yml").exists()


def test_update_cpd_ok(cpd_dir: Path) -> None:
    initialize_cpd(cpd_dir)
    update_cpd(cpd_dir)


def test_update_cpd_not_ok(cpd_dir: Path) -> None:
    initialize_cpd(cpd_dir)
    write_version_file(cpd_dir, SemanticVersion("0.0.0"))
    with pytest.raises(RuntimeError):
        update_cpd(cpd_dir)
