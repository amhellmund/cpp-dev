from conan import ConanFile
from conan.tools.files import get
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class LlvmRecipe(ConanFile):
    name = "llvm"
    version = "19.1.0"

    license = "Apache License 2.0"
    author = "LLVM"
    url = "http://llvm.org"
    description = "The LLVM Project is a collection of modular and reusable compiler and toolchain technologies."
    topics = "compiler"

    # Binary configuration
    settings = "os", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def generate(self):
        tc = CMakeToolchain(self, generator="Ninja")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(
            variables=dict(
                LLVM_ENABLE_PROJECTS=";".join(
                    [
                        "bolt",
                        "compiler-rt",
                        "clang",
                        "clang-tools-extra",
                    ]
                ),
                LLVM_ENABLE_RUNTIMES=";".join(
                    [
                        "libcxx",
                        "libcxxabi",
                        "libunwind",
                    ]
                ),
            ),
            build_script_folder="llvm",
        )
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        pass
