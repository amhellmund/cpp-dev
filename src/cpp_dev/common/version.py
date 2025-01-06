# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations

from pydantic import RootModel, model_validator

###############################################################################
# Public API                                                                ###
###############################################################################


class SemanticVersion(RootModel):
    """A semantic version string restricted to the <major>.<minor>.<patch> format.

    For details on semantic versioning, see https://semver.org/.
    """

    root: str

    @staticmethod
    def from_parts(major: int, minor: int, patch: int) -> SemanticVersion:
        """Create a semantic version from its components."""
        return SemanticVersion(root=f"{major}.{minor}.{patch}")

    @model_validator(mode="after")
    def validate_version(self) -> SemanticVersion:
        """Validate the semantic version string as part of pydantic."""
        components = self.root.split(".")
        if len(components) < 3:
            raise ValueError(
                f"Invalid semantic version string: got {self.root}, expect format <major>.<minor>.<patch>."
            )
        try:
            major, minor, patch = tuple(map(int, components))
        except ValueError as err:
            raise ValueError(
                f"Invalid semantic version string: got {self.root}, expect each part to be a number."
            ) from err
        if major < 0 or minor < 0 or patch < 0:
            raise ValueError(f"Invalid semantic version string: got {self.root}, expect each part to be positive.")

        self._major = major
        self._minor = minor
        self._patch = patch

        return self

    @property
    def major(self) -> int:
        """Return the major version."""
        return self._major

    @property
    def minor(self) -> int:
        """Return the minor version."""
        return self._minor

    @property
    def patch(self) -> int:
        """Return the patch version."""
        return self._patch

    def __eq__(self, other: object) -> bool:
        """Check if two semantic versions are equal."""
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self.root == other.root

    def __lt__(self, other: object) -> bool:
        """Compare two semantic versions."""
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __hash__(self) -> int:
        """Hash the semantic version string."""
        return hash(self.root)

    def __str__(self) -> str:
        """Return the semantic version string."""
        return self.root


class SemanticVersionWithOptionalParts:
    """A semantic version string with optional parts.

    Valid formats are "<major>", "<major>.<minor>", and "<major>.<minor>.<patch>".
    """

    @staticmethod
    def from_semantic_version(version: SemanticVersion) -> SemanticVersionWithOptionalParts:
        """Create a SemanticVersionWithOptionalParts from a SemanticVersion."""
        return SemanticVersionWithOptionalParts(version.major, version.minor, version.patch)

    def __init__(self, major: int, minor: int | None = None, patch: int | None = None) -> None:
        if minor is None and patch is not None:
            raise ValueError("Cannot specify a patch version without a minor version.")

        self._major = major
        self._minor = minor
        self._patch = patch

    @property
    def major(self) -> int:
        """Return the major version."""
        return self._major

    @property
    def minor(self) -> int | None:
        """Return the minor version."""
        return self._minor

    @property
    def patch(self) -> int | None:
        """Return the patch version."""
        return self._patch

    def __str__(self) -> str:
        return (
            f"{self.major}.{self.minor}.{self.patch}"
            if self.patch is not None
            else f"{self.major}.{self.minor}"
            if self.minor is not None
            else str(self.major)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersionWithOptionalParts):
            return NotImplemented
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
