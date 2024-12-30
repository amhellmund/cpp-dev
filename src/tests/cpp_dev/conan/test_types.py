import pytest

from cpp_dev.common.types import SemanticVersion
from cpp_dev.conan.types import ConanPackageReference


@pytest.mark.parametrize("invalid_ref", [
    "",
    "invalid_reference",
    "mypackage/@myuser/stable",
])
def test_conan_package_reference_invalid(invalid_ref):
    with pytest.raises(ValueError, match="Invalid Conan package reference:"):
        ConanPackageReference(invalid_ref)

def test_conan_package_reference_valid() -> None:
    package_ref = ConanPackageReference("name/1.2.3@user/channel")
    
    assert package_ref.name == "name"
    assert package_ref.version == SemanticVersion("1.2.3")
    assert package_ref.user == "user"
    assert package_ref.channel == "channel"
