# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from cpp_dev.common.utils import updated_env
from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.types import PackageDependency

###############################################################################
# Public API                                                                ###
###############################################################################

CONAN_HOME_ENV_VAR = "CONAN_HOME"
DEFAULT_CONAN_CHANNEL = "cppdev"


@contextmanager
def conan_env(conan_home: Path) -> Generator[None]:
    """A context manager for setting the CONAN_HOME environment variable."""
    with updated_env(**{CONAN_HOME_ENV_VAR: str(conan_home)}):
        yield


def create_conanfile(tmp_dir: Path, package_refs: list[PackageDependency]) -> Path:
    """Create a conanfile.txt with the given package dependencies."""
    conanfile_path = tmp_dir / "conanfile.txt"
    content = "[requires]\n"
    for ref in package_refs:
        content += f"{compose_conan_package_reference(ref)}\n"
    conanfile_path.write_text(content)
    return conanfile_path

def compose_conan_package_reference(ref: PackageDependency) -> str:
    """Compose a Conan package reference from a package dependency."""
    return f"{ref.parts.name}/{_get_conan_package_version(ref)}@{ref.parts.repository}/{DEFAULT_CONAN_CHANNEL}"

def _get_conan_package_version(ref: PackageDependency) -> str:
    if isinstance(ref.parts.version_spec, SemanticVersion):
        return str(ref.parts.version_spec)
    elif isinstance(ref.parts.version_spec, list):
        bound_str = " ".join([f"{bound.operand.value}{bound.version}" for bound in ref.parts.version_spec])
        return f"[{bound_str}]"
    else:
        raise ValueError("Unsupported version specification: latest")