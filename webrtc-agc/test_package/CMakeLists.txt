cmake_minimum_required(VERSION 3.9)
project(test_webrtc_agc)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_webrtc_agc src/test_webrtc_agc.c)
target_link_libraries(test_webrtc_agc ${CONAN_LIBS})
