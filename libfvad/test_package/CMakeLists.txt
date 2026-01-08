project(test_libfvad)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_libfvad src/test_libfvad.c)
target_link_libraries(test_libfvad ${CONAN_LIBS})