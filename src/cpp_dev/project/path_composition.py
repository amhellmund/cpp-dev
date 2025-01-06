# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from pathlib import Path

###############################################################################
# Public API                                                                ###
###############################################################################


def compose_project_config_file(project_dir: Path) -> Path:
    """Compose the path to the project"s configuration file."""
    return project_dir / "cpp-dev.yaml"


def compose_project_lock_file(project_dir: Path) -> Path:
    """Compose the path to the project"s lock file."""
    return project_dir / "cpp-dev.lock"


def compose_include_file(project_dir: Path, name: str, *components: str) -> Path:
    """Compose the path to an include file."""
    return (project_dir / "include" / name).joinpath(*components)


def compose_source_file(project_dir: Path, *components: str) -> Path:
    """Compose the path to a source file."""
    return (project_dir / "src").joinpath(*components)
