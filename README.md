# cpp-dev

The setup of a new C++ project typically involves several decisions and, consequently, a considerable amount of setup code to be written to get the first line executed. 

- C++ standard
- Compiler toolchain
- Package management
- Build system
- Test framework
- Code coverage
- Static code analysis
- Sanitizers

Additionally, sharing of useful components with other developers and projects is harder compared to other languages' ecosystems due to the huge range of configuration possibilities.

The project **cpp-dev** (short: cpd) is an attempt to bridge the "perceived" gap to other languages by providing a simple tool to accomplish the goals mentioned above.


# Design Principle: Simplicity-over-Configurability

The C++ ecosystem provides an immense set of tools to support and execute the software engineering process.
**cpp-dev** follows the design principle to limit the configurability (e.g. supported tool chain, OS package manager, pre-defined project setup, etc.) to achieve a simplistic, but effective and efficient development process.

**cpp-dev** will use the following external tools in its early phase to prove usability in a proof-of-concept approach.
Some of these tools will later be replaced by either different tools or custom implementations.

- Operating System: Ubuntu 22.04
- Package Management (for base packages like boost): Custom (based on apt packages)
- Build System: Custom
- Toolchain: LLVM-based (clang, clang-format, clang-tidy, clang-sanitizer)
- Test framework: gtest and gmock


# Workflow

A workflow using **cpp-dev** could look like:

* **Initialize project**: `cpd init <new-project> [--std c++17] [--version <major.minor.patch>]`
* **Add dependency**: `cpd add-dep <dep>@<version>`
* **Build**: `cpd build [release | debug]`
* **Execute**: `cpd execute [release | debug]`
* **Check**: `cpd check`
* **Format**: `cpd format`
* **Test**: `cpd test [--show-coverage]`
* **Packaging**: `cpd package`
* **List Packages**: `cpd list-packages`


# Package Structure

Simplification by convention is a common principle in the software engineering community.
**cpp-dev** therefore provides a common package structure convention:

```
<root>
|_ cpp-dev.yaml
|_ src
   |_ executables
      |_ exec1.cpp
   |_ lib.cpp
   |_ lib.test.cpp
|_ include
   |_ <package-name>
      |_ lib.hpp
```

The source files listed in the `src/executables` folder are assumed to be stand-alone executables.
Each of these file gets converted into a dedicated executable, e.g. `exec1.cpp` would become the executable with name `exec1`.
All other files outside of the `executables` folder are assumed to be library sources and get compiled into the library `lib<package-name>`.
Each **cpp-dev** package initially supports only a single library per package.

## Header-Only

Header-only packages only provide header files in the top-level `include` folder.
Tests are then stored in the top-level `src` folder.


# Configuration File

The **cpp-dev** configuration file has the following structure:

```
name: <package-name>
author: <author>
version:
   major: 0
   minor: 1
   patch: 0
license: <software-license>

std: 20

dependencies:
   - name: boost
     repository: official
     version:
         major: 1
         minor: 83
         patch: 2
```


# FAQ

* *Why another tool to increase the already high complexity of the tool landscape?* C++ is a lovely wonderful language, but getting started has a too high complexity in my opinion. I would love to implement more smaller utilities using some of the great features of later C++ standards, but the reusability is often harder for smaller (private) projects. Other ecosystems nicely show that good tooling can be really simple to use.
  
* *Why the hell is the tool written in Python and not C++?* I really love C++ with all its magic and power, but bootstrapping a new project has a too high complexity. Python is thereby a good example for how the tooling could look like. Maybe, later, this tool is even written in Rust for performance reasons.

* *Who is the target audience of the tool?* C++ experts already have their setup with pre-defined templates for the different tools (CMake, Clang, etc.), but people who want to start exploring the power of C++ (hopefully, there are still people who want to learn C++) could find this tooling helpful.

* *Why is there a hard limitation to Ubuntu 22.04?* Ubuntu is probably still one of the mostly used Linux-based operating systems having a good and simple tooling for installing system-wide dependencies. The goal right now is to build an MVP to see if there is even a future for such a tooling. If the tooling turns out to be useful, the limitations would obviously be relaxed to reach more people.


# How-to Contribute

**cpp-dev** is currently in an early development and evaluation phase.
Contributions are welcome in terms of code contributions, conceptual feedback ("the idea is bulls**t is also a highly valued feedback if good arguments are given) and additional ideas.