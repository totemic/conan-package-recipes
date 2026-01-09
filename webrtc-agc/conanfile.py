#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class WebRtcAgcConan(ConanFile):
    name = "webrtc-agc"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    topics = ("audio", "agc", "webrtc", "automatic-gain-control", "voice")
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    homepage = "https://github.com/cpuimage/WebRTC_AGC"
    url = "https://github.com/totemic/conan-package-recipes/tree/main/webrtc-agc"
    license = "BSD-3-Clause"
    description = "Standalone port of WebRTC's Automatic Gain Control (AGC) module"
    _source_subfolder = "sources"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt.patch"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        # Using the latest commit from master branch
        # You can pin to a specific commit hash for reproducibility
        tools.get("https://github.com/cpuimage/WebRTC_AGC/archive/refs/heads/master.tar.gz",
                  strip_root=True, destination=self._source_subfolder)

        # Alternative: pin to a specific commit
        # commit_hash = "abc123..."
        # tools.get(f"https://github.com/cpuimage/WebRTC_AGC/archive/{commit_hash}.tar.gz",
        #           sha256="...", strip_root=True, destination=self._source_subfolder)

    def build(self):
        # Apply patch to create library target instead of just executable
        tools.patch(base_path=self._source_subfolder, patch_file="CMakeLists.txt.patch")

        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        # Copy license
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)

        # Copy headers
        self.copy("agc.h", dst="include", src=self._source_subfolder, keep_path=False)

        # Copy library files from the build folder
        # During package(), the current folder is the build folder
        self.copy("libwebrtc_agc.a", dst="lib", src=".", keep_path=False)
        self.copy("libwebrtc_agc.lib", dst="lib", src=".", keep_path=False)
        self.copy("libwebrtc_agc.so*", dst="lib", src=".", keep_path=False)
        self.copy("libwebrtc_agc.dylib", dst="lib", src=".", keep_path=False)
        self.copy("webrtc_agc.dll", dst="bin", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["webrtc_agc"]
        self.cpp_info.names["cmake_find_package"] = "webrtc-agc"
        self.cpp_info.names["cmake_find_package_multi"] = "webrtc-agc"

        # On some platforms, may need math library
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["m"]
