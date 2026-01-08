#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class SileroVadConan(ConanFile):
    name = "silero-vad"
    version = "5.0"
    settings = "os", "compiler", "build_type", "arch"
    topics = ("audio", "vad", "voice", "detection", "onnx", "ml")
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    homepage = "https://github.com/snakers4/silero-vad"
    url = "https://github.com/totemic/conan-package-recipes/tree/main/silero-vad"
    license = "MIT"
    description = "Silero VAD: pre-trained enterprise-grade Voice Activity Detector"
    _source_subfolder = "sources"
    generators = "cmake"
    exports = ["LICENSE.md"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        # ONNX Runtime is expected to be provided externally (not via Conan)
        # User must set CMAKE_PREFIX_PATH to onnxruntime installation
        pass

    def source(self):
        # Download the source repository
        tools.get("https://github.com/snakers4/silero-vad/archive/refs/tags/v{}.tar.gz".format(self.version),
                  sha256="f4a4910b8dafd5228d1bd3c69b2d98d730a6037c0cb89ed3943020e77ae1cef8")
        extracted_dir = "%s-%s" % (self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

        # Patch the C++ example for compatibility with newer ONNX Runtime
        cpp_file = os.path.join(self._source_subfolder, "examples/cpp/silero-vad-onnx.cpp")

        # Replace the Session initialization with platform-specific code
        tools.replace_in_file(cpp_file,
                             "        session = std::make_shared<Ort::Session>(env, model_path.c_str(), session_options);",
                             """#ifdef _WIN32
        session.reset(new Ort::Session(env, model_path.c_str(), session_options));
#else
        std::string model_path_str(model_path.begin(), model_path.end());
        session.reset(new Ort::Session(env, model_path_str.c_str(), session_options));
#endif""")

        # Download the ONNX model file
        model_dir = os.path.join(self._source_subfolder, "model")
        os.makedirs(model_dir, exist_ok=True)
        tools.download("https://github.com/snakers4/silero-vad/raw/master/src/silero_vad/data/silero_vad.onnx",
                      os.path.join(model_dir, "silero_vad.onnx"))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        # Pass CMAKE_PREFIX_PATH from environment to find external onnxruntime
        if os.environ.get("CMAKE_PREFIX_PATH"):
            cmake.definitions["CMAKE_PREFIX_PATH"] = os.environ.get("CMAKE_PREFIX_PATH")

        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        # Create a CMakeLists.txt for the C++ example
        cmake_content = """cmake_minimum_required(VERSION 3.15)
project(silero-vad CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find ONNX Runtime (expected to be provided externally)
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

# Create library from the C++ example
add_library(${PROJECT_NAME} examples/cpp/silero-vad-onnx.cpp)
target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/examples/cpp>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${ONNXRUNTIME_INCLUDE_DIR}
)

# Link against ONNX Runtime
target_link_libraries(${PROJECT_NAME} PUBLIC ${ONNXRUNTIME_LIB})

# Installation
install(TARGETS ${PROJECT_NAME}
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES examples/cpp/wav.h
    DESTINATION include/silero-vad
)

# Install model file
install(FILES model/silero_vad.onnx
    DESTINATION share/silero-vad/models
)
"""
        tools.save(os.path.join(self._source_subfolder, "CMakeLists.txt"), cmake_content)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        # Copy license
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["silero-vad"]  # onnxruntime is external, not included in this package
        self.cpp_info.names["cmake_find_package"] = "SileroVAD"
        self.cpp_info.names["cmake_find_package_multi"] = "SileroVAD"
        self.cpp_info.includedirs = ["include/silero-vad"]

        # Set the model path as a variable
        model_path = os.path.join(self.package_folder, "share", "silero-vad", "models", "silero_vad.onnx")
        self.cpp_info.defines.append('SILERO_VAD_MODEL_PATH="{}"'.format(model_path))

        # ONNX Runtime is required for linking
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")

        # Inform users that ONNX Runtime is required externally
        self.output.info("IMPORTANT: This package requires ONNX Runtime to be installed externally")
        self.output.info("Set CMAKE_PREFIX_PATH or LD_LIBRARY_PATH to your onnxruntime installation")
