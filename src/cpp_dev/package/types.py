# Copyright 2024 Andi Hellmund
#
# Licensed under the BSD 3-Clause License


from cpp_dev.common.types import SemanticVersion


class PackageRef:
    def __init__(self, ref: str):
        components = ref.split("-")
        self.repository = components[0]
        self.name = components[1]
        self.version = SemanticVersion(components[2])

    def __repr__(self) -> str:
        return f"{self.repository}-{self.name}-{self.version}"
