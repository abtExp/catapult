cmake_minimum_required(VERSION 3.13)

set(CMAKE_CXX_STANDARD 23) # Enable the C++23 standard

project(txtedit)

# Add source files from src folder
file(GLOB_RECURSE SOURCE_FILES src/*.cpp)

# Add header files from include folder
include_directories(include)

# Build the executable
add_executable(txtedit main.cpp ${SOURCE_FILES})