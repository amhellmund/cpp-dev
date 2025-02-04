import pytest

from cpp_dev.common.version import SemanticVersion
from cpp_dev.dependency.conan.types import \
    ConanPackageReferenceWithSemanticVersion


@pytest.mark.parametrize("invalid_ref", [
    "",
    "invalid_reference",
    "mypackage/@myuser/stable",
])
def test_conan_package_reference_invalid(invalid_ref):
    with pytest.raises(ValueError, match="Invalid Conan package reference:"):
        ConanPackageReferenceWithSemanticVersion(invalid_ref)

def test_conan_package_reference_valid() -> None:
    package_ref = ConanPackageReferenceWithSemanticVersion("name/1.2.3@user/channel")
    
    assert package_ref.name == "name"
    assert package_ref.version == SemanticVersion("1.2.3")
    assert package_ref.user == "user"
    assert package_ref.channel == "channel"
