# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from pathlib import Path


def compose_project_config_file(project_dir: Path) -> Path:
    return project_dir / "cpp-dev.yaml"


def compose_include_file(project_dir: Path, name: str, *components: str) -> Path:
    return (project_dir / "include" / name).joinpath(*components)


def compose_source_file(project_dir: Path, *components: str) -> Path:
    return (project_dir / "src").joinpath(*components)


def compose_env_dir(project_dir: Path) -> Path:
    return project_dir / ".env"


def compose_env_bin_dir(env_dir: Path) -> Path:
    return env_dir / "bin"


def compose_env_lib_dir(env_dir: Path) -> Path:
    return env_dir / "lib"


def compose_env_include_dir(env_dir: Path) -> Path:
    return env_dir / "include"


def compose_env_link_index_dir(env_dir: Path) -> Path:
    return env_dir / ".link_index"
