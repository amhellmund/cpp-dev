# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License

from __future__ import annotations

from typing import Literal

from pydantic import RootModel, ValidationError, model_validator


CppStandard = Literal["c++11", "c++14", "c++17", "c++20", "c++23"]


class SemanticVersion(RootModel):
    root: str

    @model_validator(mode="after")
    def validate_version(self) -> SemanticVersion:
        components = self.root.split(".")
        if len(components) != 3:
            raise ValidationError(
                f"Invalid semantic version string: got {self.root}, expected <major>.<minor>.<patch>"
            )

        major, minor, patch = map(int, components)
        if major < 0 or minor < 0 or patch < 0:
            raise ValidationError(
                f"Invalid semantic version string: got {self.root}, expected positive integers"
            )

        return self
