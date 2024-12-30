# Copyright (c) 2024 Andi Hellmund. All rights reserved.

# This work is licensed under the terms of the BSD-3-Clause license.
# For a copy, see <https://opensource.org/license/bsd-3-clause>.

import re

from cpp_dev.common.types import SemanticVersion

###############################################################################
# Public API                                                                ###
###############################################################################

 
class ConanPackageReference:
    CONAN_REFERENCE_PATTERN = r"(?P<name>[a-zA-Z0-9_]+)/(?P<version>\d+\.\d+\.\d+)@(?P<user>[a-zA-Z0-9_]+)/(?P<channel>[a-zA-Z0-9_]+)"

    def __init__(self, ref_str: str) -> None:
        """
        Initialize a ConanPackageReference object.

        This method parses a Conan package reference string and extracts its components.
        It also validates the semantic version format. A Conan package reference has the format:

            name/version@user/channel
        """
        match = re.match(self.CONAN_REFERENCE_PATTERN, ref_str)
        if not match:
            raise ValueError(f"Invalid Conan package reference: {ref_str}")

        self.name = match.group('name')
        self.version = SemanticVersion(match.group('version'))
        self.user = match.group('user')
        self.channel = match.group('channel')

    def __str__(self) -> str:
        return f"{self.name}/{self.version}@{self.user}/{self.channel}"