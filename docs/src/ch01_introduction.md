# Introduction

The setup of a new C++ project typically involves several decisions and, consequently, a considerable amount of setup code to be written to get the first line executed. 

- C++ standard
- Compiler toolchain
- Package management
- Build system
- Test framework
- Code coverage
- Static code analysis
- Sanitizers

Additionally, sharing of useful components with other developers and projects is harder compared to other languages" ecosystems due to the huge range of configuration possibilities.

The project **cpp-dev** (short: `cpd`) is an attempt to bridge the *perceived* gap to other languages by providing a tool to accomplish the goals mentioned above.


# Design Principle: Simplicity-over-Configurability

The C++ ecosystem provides an large set of tools to support and execute the software engineering process.
**cpp-dev** follows the design principle to limit the configurability (e.g. supported tool chain, package manager, pre-defined project setup, etc.) to achieve a simplistic, but effective and efficient development process.

**cpp-dev** is designed as a tool around the following external tools:

- Package Management: Conan2
- Build System: Ninja
- Toolchain: LLVM-based (clang, clang-format, clang-coverage, clang-sanitizer, clang-tidy)
- Test framework: gtest and gmock
- Code coverage: lcov

> **_INFO:_** **cpd-dev** will initially support only Ubuntu 24.04 (LTS) as operating system.
> Later, once the proof-of-concept phase is over, additional operating systems and distributions will be supported.


## Not Yet-Another-Dependency-Manager

There have been a lot of good attempts in the community to create feature-rich package managers for C++ with Conan2 being one of the most prominent ones.
**cpp-dev** does not and will not introduce another package manager, but use Conan2 as a fundamental building block.
All packages consumed by and created by **cpp-dev** are proper Conan packages stored in a proper Conan remote (e.g. JFrog Artifactory).
Therefore, all **cpp-dev** packages may also be used outside of **cpp-dev** as well, for example with plain CMake projects, when combined with Conan, of course.


# Workflow

A workflow using **cpp-dev** could look like:

* **Initialize project**: `cpd init <new-project> [--std c++17] [--version <major.minor.patch>]`
* **Add external dependency**: `cpd add-dep <dep>@<version>`
* **Update external dependencies**: `cpd update-dep [<dep>@<version>]`
* **Build**: `cpd build [release | debug]`
* **Execute**: `cpd execute [release | debug]`
* **Check**: `cpd check`
* **Format**: `cpd format`
* **Test**: `cpd test [--show-coverage]`
* **Tests with compiler sanitiziers**: `cpd test-sanitize`
* **Packaging (incl. uploading)**: `cpd package`
* **List Packages**: `cpd list-packages`


# Package Structure

Simplification by convention is a common principle in the software engineering community.
**cpp-dev** therefore provides and expects a common package structure convention:

```
<root>
|_ cpp-dev.yaml
|_ src
   |_ executables
      |_ exec.cpp
   |_ <package-name>.cpp
   |_ <package-name>.test.cpp
|_ include
   |_ <package-name>
      |_ <package-name>.hpp
```

The source files listed in the `src/executables` folder are assumed to be stand-alone executables.
Each of these file gets converted into a dedicated executable, e.g. `exec.cpp` would become the executable with name `exec`.
All other C++ files outside of the `executables` folder are assumed to be library sources and get compiled into the library `lib<package-name>`.
Each **cpp-dev** package supports only a single library per package.

## Header-Only

Header-only packages only provide header files in the top-level `include` folder.
Tests are then stored in the top-level `src` folder.


# Configuration File

The **cpp-dev** configuration file has the following structure (currently re-worked):

```
name: <package-name>
author: <author>
version: 0.1.0
license: <software-license>

std: 20

dependencies:
   - name: boost
     channel: official
     version: 1.83.2
```