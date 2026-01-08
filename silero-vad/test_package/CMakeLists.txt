cmake_minimum_required(VERSION 3.15)
project(test_silero_vad CXX)

set(CMAKE_CXX_STANDARD 17)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Find ONNX Runtime (external dependency, not from Conan)
find_path(ONNXRUNTIME_INCLUDE_DIR onnxruntime_cxx_api.h
    HINTS ${CMAKE_PREFIX_PATH}
    PATH_SUFFIXES include include/onnxruntime/core/session
)
find_library(ONNXRUNTIME_LIB NAMES onnxruntime
    HINTS ${CMAKE_PREFIX_PATH}
    PATH_SUFFIXES lib
)

if(NOT ONNXRUNTIME_INCLUDE_DIR OR NOT ONNXRUNTIME_LIB)
    message(FATAL_ERROR "ONNX Runtime not found. Set CMAKE_PREFIX_PATH to onnxruntime installation")
endif()

add_executable(${PROJECT_NAME} src/test_silero_vad.cpp)
target_include_directories(${PROJECT_NAME} PRIVATE ${ONNXRUNTIME_INCLUDE_DIR})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${ONNXRUNTIME_LIB})
