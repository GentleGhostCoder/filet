# this Cmakelist.txt is optional and not required for c++ development (ide ->
# autocompletion) dependencies evaluation.
cmake_minimum_required(VERSION 3.4...3.22)
project(cpputils LANGUAGES CXX)

set(DEBUG_MODE=1)
set(CMAKE_CXX_STANDARD 17)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
include_directories(${PYTHON_INCLUDE_DIRS})

set(PROJECT_DIR cpputils)
set(EXT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib)
set(VENV_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.venv")

# Set the path to the Python interpreter in the virtual environment
set(PYTHON_EXECUTABLE "${VENV_PATH}/bin/python")

execute_process(
  COMMAND
    ${PYTHON_EXECUTABLE} -c
    "import pkg_resources; print(f'{pkg_resources.get_distribution(\"pybind11\").location}/pybind11/share/cmake')"
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(pybind11 REQUIRED PATHS ${pybind11_DIR})
find_package(
  Python3
  COMPONENTS Interpreter Development
  REQUIRED)

include_directories(${PROJECT_DIR})
include_directories(${EXT_DIR})
include_directories(${EXT_DIR}/rapidjson/include)
include_directories(${EXT_DIR}/catch2/target/include)

get_property(
  dirs
  DIRECTORY .
  PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "dir='${dir}'")
endforeach()

file(GLOB_RECURSE SOURCE_FILES *.cpp)
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*ext.*")
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*test.*")
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*cmake-build-debug.*")

pybind11_add_module(${PROJECT_NAME} MODULE NO_EXTRAS ${SOURCE_FILES})

set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME ${PROJECT_NAME})
target_compile_definitions(${PROJECT_NAME} PRIVATE VERSION_INFO=${VERSION_INFO})

# Enable testing and add the test directory
enable_testing()

list(APPEND CMAKE_MODULE_PATH "${EXT_DIR}/catch2/extras")
add_subdirectory(lib/catch2)

# Look for Catch2 package in the system find_package(Catch2 REQUIRED)

# Add the test executable set(TEST_SOURCES ${SOURCE_FILES}) list(FILTER
# TEST_SOURCES EXCLUDE REGEX ".*bindings.*")
file(GLOB_RECURSE TEST_SOURCES cpputils/*)
file(GLOB_RECURSE TEST_FILES cpputils/tests/*.cpp)
add_executable(tests ${TEST_SOURCES} ${TEST_FILES})

# Link Catch2 for testing
target_link_libraries(tests PRIVATE Catch2::Catch2 pybind11::pybind11
                                    pybind11::embed)

# Register tests with CTest
include(CTest)
include(Catch)
catch_discover_tests(tests)

add_compile_options(
  "-Wall"
  "-Wpedantic"
  "-Wextra"
  "-fexceptions"
  "$<$<CONFIG:DEBUG>:-O0;-g3;-ggdb>"
  "-Wextra"
  "-Wundef"
  "-pedantic"
  "-msse2"
  "-msse3"
  "-mpopcnt"
  "-funsafe-math-optimizations"
  "-fno-math-errno")
