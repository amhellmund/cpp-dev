# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.


from __future__ import annotations

from pydantic import RootModel, model_validator

from cpp_dev.common.version import SemanticVersion

from .specifier_parser import DependencyParserError, parse_dependency_string
from .types import DependencySpecifierParts

###############################################################################
# Public API                                                                ###
###############################################################################


class DependencySpecifier(RootModel):
    """A package dependency specifier.

    Each package dependency is a string in the format '<repository>/<name>[<version_spec>]'.
    The parameter <repository> is the user or organization that owns the dependency.
    The default value for <repository> is 'official'.
    The <name> of the dependency is mandatory.
    The <version_spec> supports an exact version, lower/upper bounds, intervals or 'latest'.
    The default value for <version_spec> is latest.
    The exact version is specified as '<major>.<minor>.<patch>', while lower/upper bounds and intervals
    use the format '< | <= | > | >= <major>[.<minor>[.<patch>]]' with minor and parts parts being optional.
    """

    @staticmethod
    def from_parts(parts: DependencySpecifierParts) -> DependencySpecifier:
        """Create a package dependency from its parts."""
        repository_str = f"{parts.repository}/" if parts.repository is not None else ""
        version_spec = "latest"
        if isinstance(parts.version_spec, SemanticVersion):
            version_spec = str(parts.version_spec)
        elif isinstance(parts.version_spec, list):
            bounds_str = [f"{bound.operand.value}{bound.version}" for bound in parts.version_spec]
            version_spec = ",".join(bounds_str)
        return DependencySpecifier(f"{repository_str}{parts.name}[{version_spec}]")

    root: str

    @model_validator(mode="after")
    def validate_version(self) -> DependencySpecifier:
        """Validate the package dependency str as part of pydantic."""
        try:
            self._parts = parse_dependency_string(self.root)
        except DependencyParserError as err:
            raise ValueError(
                f"Invalid package depdency string: got {self.root}.",
            ) from err
        return self

    @property
    def parts(self) -> DependencySpecifierParts:
        """Return the parts of the package dependency.

        The parts contain:
        o Repository
        o Name
        o Version Specs
        """
        return self._parts

    def __eq__(self, other: object) -> bool:
        """Check if two semantic versions are equal."""
        if not isinstance(other, DependencySpecifier):
            return NotImplemented
        return self.root == other.root

    def __hash__(self) -> int:
        """Hash the semantic version string."""
        return hash(self.root)

    def __str__(self) -> str:
        """Return the semantic version string."""
        return self.root
