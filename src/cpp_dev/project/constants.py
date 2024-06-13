# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

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
