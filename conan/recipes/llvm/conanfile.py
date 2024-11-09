import os

from conan import ConanFile
from conan.tools.files import collect_libs, copy, get
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files.symlinks import absolute_to_relative_symlinks


class LlvmRecipe(ConanFile):
    name = "llvm"
    major = 19
    minor = 1
    patch = 0
    version = f"{major}.{minor}.{patch}"

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
                        "clang",
                        "clang-tools-extra",
                        "compiler-rt",
                        "lld",
                        "lldb",
                        "openmp",
                    ]
                ),
                LLVM_ENABLE_RUNTIMES=";".join(
                    [
                        "libcxx",
                        "libcxxabi",
                        "libunwind",
                    ]
                ),
                CLANG_DEFAULT_CXX_STDLIB="libc++",
                CLANG_DEFAULT_LINKER="lld",
                CLANG_DEFAULT_RTLIB="compiler-rt",
                CLANG_DEFAULT_UNWINDLIB="libunwind",
                CLANG_DEFAULT_OPENMP_RUNTIME="libomp",
            ),
            build_script_folder="llvm",
        )
        cmake.build()

    def package(self):
        # The package function is not relying on the CMake install functionality due to the large
        # size of static libraries within the LLVM install folder. Instead, the relevant libraries
        # get copied manually.
        copy_specs = {
            "bin": [
                "clang",
                "clang++",
                f"clang-{LlvmRecipe.major}",
                "clangd",
                r"ld64.lld",
                r"ld.lld",
                "lld",
                "lldb",
            ],
            "include": [
                r"c++/**",
            ],
            f"lib/clang/{LlvmRecipe.major}": [
                "include/**",
                "lib/**",
            ],
            "lib": [
                r"libclang-cpp.so*",
                r"libclang.so*",
                r"liblldb.so*",
                r"libLTO.so*",
            ],
        }
        if self.settings.os == "Linux" and self.settings.arch == "x86_64":
            copy_specs["include/x86_64-unknown-linux-gnu"] = [
                r"c++/**/*",
            ]
            copy_specs["lib/x86_64-unknown-linux-gnu"] = [
                r"libc++*",
                r"lib*omp*",
                r"libunwind*",
            ]

        for dir_path, patterns in copy_specs.items():
            for pattern in patterns:
                copy(
                    self,
                    pattern=pattern,
                    src=os.path.join(self.build_folder, dir_path),
                    dst=os.path.join(self.package_folder, dir_path),
                )
        # Absolute symlinks get converted into relative ones
        absolute_to_relative_symlinks(self, self.package_folder)

    def package_info(self):
        bin_dir = os.path.join(self.package_folder, "bin")

        self.cpp_info.bindirs = [bin_dir]
        self.runenv_info.append_path("PATH", bin_dir)
        self.buildenv_info.append_path("PATH", bin_dir)

        lib_dir = os.path.join(self.package_folder, "lib")
        lib_dirs = [lib_dir]
        if self.settings.arch == "x86_64" and self.settings.os == "Linux":
            lib_dirs.append(os.path.join(lib_dir, "x86_64-unknown-linux-gnu"))
        self.cpp_info.libdirs = lib_dirs

        self.cpp_info.libs = collect_libs(self)
