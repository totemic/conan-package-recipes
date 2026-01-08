#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class LibEBUR128Conan(ConanFile):
    name = "libebur128"
    version = "1.2.6"
    settings = "os", "compiler", "build_type", "arch"
    topics = ("audio", "loudness", "ebur128", "bs1770", "lufs")
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    homepage = "https://github.com/jiixyj/libebur128"
    url = "https://github.com/totemic/conan-package-recipes/tree/main/libebur128"
    license = "MIT"
    description = "A library implementing the EBU R128 loudness standard"
    _source_subfolder = "sources"
    generators = "cmake"
    exports = ["LICENSE.md"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        release_name = "v%s" % self.version
        tools.get("https://github.com/jiixyj/libebur128/archive/{}.tar.gz".format(release_name),
                  sha256="baa7fc293a3d4651e244d8022ad03ab797ca3c2ad8442c43199afe8059faa613")
        extracted_dir = "%s-%s" % (self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        
        # Configure CMake options
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ENABLE_INTERNAL_QUEUE_H"] = "ON"  # Use internal queue implementation
        
        cmake.configure(source_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
        # Copy license
        self.copy("COPYING", dst="licenses", src=self._source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ebur128"]
        self.cpp_info.names["cmake_find_package"] = "libebur128"
        self.cpp_info.names["cmake_find_package_multi"] = "libebur128"
        
        # Add math library for non-Windows platforms
        if self.settings.os != "Windows":
            self.cpp_info.system_libs.append("m")