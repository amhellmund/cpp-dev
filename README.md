# cpp-dev

![CI Pipeline](https://img.shields.io/github/actions/workflow/status/amhellmund/cpp-dev/ci.yml?label=CI%20Pipeline)
![Documentation Pipeline](https://img.shields.io/github/actions/workflow/status/amhellmund/cpp-dev/documentation.yml?label=Documentation)

The project **cpp-dev** (short: **cpd**) combines existing state-of-the-art C++ tooling
to ease the development and exchange of C++ libraries across different platforms.
The ultimate long-term goal is to achieve a development workflow comparable with the
ecosystems of other programming languages (e.g. Rust or Python).

> **_WARN:_**  
> This project is currently work in progress and not yet in a functional state.
> Please check the feature table below about which features are already supported.


## Documentation

Please check the complete documentation at: [cpp-dev documentation](https://amhellmund.github.io/cpp-dev/).


## Getting Started

> **_INFO_:**
> This project currently only supports Ubuntu 24.04.
> This hard requirement will get dropped after a first release is made availabe to have some value-add initially (guideline: feature completeness before increasing the operating system support).


### Setup

This project is not yet available as official Python package due to the early development state.
Therefore, testing out **cpp-dev** requires the source code to be checked out locally.
The pre-requisite to run **cpp-dev** is to have the Python ``uv`` tool installed on your machine - please follow the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for fruther instructions.
Afterwards, call the following command to check that **cpd** is properly installed.

```console
uv run cpd version
cpp-dev version 0.0.1
```

Alternatively, use the virtual environment to directly use the ``cpd`` cli.

```console
uv sync
source .venv/bin/activate
(cpp-dev) cpd version
cpp-dev version 0.0.1
```

## Workflow

The documentation of the high-level workflow assumes that the environment is setup with the Python venv sourced in your shell (instead of using the ``uv run`` wrapper).


## Feature Status

The tables below show the status for features and operating systems.


### Features

| Feature                |                             Status                             |
| ---------------------- | :------------------------------------------------------------: |
| Tool Initialization    |  ![Completed](https://img.shields.io/badge/completed-027148)   |
| Project Initialization | ![InProgress](https://img.shields.io/badge/in_progress-00008B) |


### Operating Systems

| Operating System |                           Status                            |
| ---------------- | :---------------------------------------------------------: |
| Ubuntu 24.04     | ![Supported](https://img.shields.io/badge/supported-027148) |
    

## External Tools

**cpp-dev** is designed as a tool around the following external tools:

- Package Management: Conan2
- Build System: Ninja
- Toolchain: LLVM-based (clang, clang-format, clang-coverage, clang-sanitizer, clang-tidy)
- Test framework: gtest and gmock
- Code coverage: lcov


### Compatibility

**cpp-dev** uses Conan2 as package management such that all packages created by **cpp-dev** are usable in other configurations for which Conan2 generators exist, e.g. CMake.


## FAQ

* *Why another tool to increase the already high complexity of the tool landscape?*
  C++ is a lovely wonderful language, but getting started has a too high complexity in my opinion.
  I would love to implement smaller utilities using some of the great features of later C++ standards, but the reusability is often harder for smaller (private) projects.
  Other ecosystems nicely show that good tooling can be really simple to use.
  
* *Why the hell is the tool written in Python and not C++?*
  I really love C++ with all its magic and power, but bootstrapping a new project has a too high complexity.
  Python is thereby a good example for how the tooling could look like.
  Additionally, this tool uses Conan2 intensively which is written in Python.

* *Who is the target audience of the tool?*
  C++ experts already have their setup with pre-defined templates for the different tools (CMake, Clang, etc.), but people who want to start exploring the power of C++ (hopefully, there are still people who want to learn C++) could find this tooling helpful.

* *Why is there a hard limitation to Ubuntu 24.04?*
  Ubuntu is probably still one of the mostly used Linux-based operating systems.
  The goal right now is to build a proof-of-concept to see if there is even a future for such a tooling.
  If the tooling turns out to be useful, the limitations would obviously be relaxed to reach more people.


## How-to Contribute

**cpp-dev** is currently in an early development and evaluation phase.
Contributions are welcome in terms of code contributions, conceptual feedback ("the idea is bulls**t is also a highly valued feedback if good arguments are given) and additional ideas.