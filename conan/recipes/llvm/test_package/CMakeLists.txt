cmake_minimum_required(VERSION 3.28)
project(LlvmTestPackage CXX)

add_executable(testllvm17 src/std17.cpp)
set_property(TARGET testllvm17 PROPERTY CXX_STANDARD 17)

add_executable(testllvm20 src/std20.cpp)
set_property(TARGET testllvm20 PROPERTY CXX_STANDARD 20)