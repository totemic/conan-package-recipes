#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class LibfvadConan(ConanFile):
    name = "libfvad"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    topics = ("audio", "vad", "voice", "detection", "webrtc")
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    homepage = "https://github.com/dpirch/libfvad"
    url = "https://github.com/totemic/conan-package-recipes/tree/main/libfvad"
    license = "MIT"
    description = "Voice Activity Detection (VAD) library based on WebRTC"
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
        tools.get("https://github.com/dpirch/libfvad/archive/{}.tar.gz".format(release_name),
                  sha256="8c8a1e4911a454b1a8e3ed062abbce4865eea3fc794417e2c96373309174215c")
        extracted_dir = "%s-%s" % (self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = self.options.fPIC
            
            # Configure autotools
            self.run("autoreconf -i")
            
            args = []
            if self.options.shared:
                args.extend(['--enable-shared', '--disable-static'])
            else:
                args.extend(['--disable-shared', '--enable-static'])
                
            env_build.configure(args=args)
            env_build.make()

    def package(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.install()
            
        # Copy license
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["fvad"]
        self.cpp_info.names["cmake_find_package"] = "libfvad"
        self.cpp_info.names["cmake_find_package_multi"] = "libfvad"
