# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

from __future__ import annotations

import re

from pydantic import RootModel, model_validator

from cpp_dev.common.version import SemanticVersion

###############################################################################
# Public API                                                                ###
###############################################################################


class ConanPackageReferenceWithVersionRanges(str):
    """A generic Conan package reference supporting version ranges.
    
    This package reference has the format: name/[version_ranges]@user/channel.
    """

 
class ConanPackageReferenceWithSemanticVersion(RootModel):
    """A Conan package reference in the format name/version@user/channel."""
    
    root: str

    @model_validator(mode="after")
    def validate_reference(self) -> ConanPackageReferenceWithSemanticVersion:
        CONAN_REFERENCE_PATTERN = r"(?P<name>[a-zA-Z0-9_]+)/(?P<version>\d+\.\d+\.\d+)@(?P<user>[a-zA-Z0-9_]+)/(?P<channel>[a-zA-Z0-9_]+)"
        match = re.match(CONAN_REFERENCE_PATTERN, self.root)
        if not match:
            raise ValueError(f"Invalid Conan package reference: {self.root}")

        self._name = match.group("name")
        self._version = SemanticVersion(match.group("version"))
        self._user = match.group("user")
        self._channel = match.group("channel") 

        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> SemanticVersion:
        return self._version
    
    @property
    def user(self) -> str:
        return self._user
    
    @property
    def channel(self) -> str:
        return self._channel

    def __hash__(self) -> int:
        return hash(self.root)

    def __str__(self) -> str:
        return f"{self._name}/{self._version}@{self._user}/{self._channel}"
    