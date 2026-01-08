#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class TestSileroVadConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Pass CMAKE_PREFIX_PATH from environment to find external onnxruntime
        if os.environ.get("CMAKE_PREFIX_PATH"):
            cmake.definitions["CMAKE_PREFIX_PATH"] = os.environ.get("CMAKE_PREFIX_PATH")
        cmake.configure()
        cmake.build()

        # Fix rpath on macOS to find onnxruntime dylib in same directory
        if self.settings.os == "Macos":
            import subprocess
            exe_path = os.path.join(self.build_folder, "bin", "test_silero_vad")
            if os.path.exists(exe_path):
                # Add @executable_path to rpath so it finds dylibs in same directory
                subprocess.run(["install_name_tool", "-add_rpath", "@executable_path", exe_path], check=False)

    def imports(self):
        import shutil
        import glob

        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")
        self.copy("*.onnx", dst="models", src="share/silero-vad/models")

        # Copy external onnxruntime dylib if CMAKE_PREFIX_PATH is set
        if os.environ.get("CMAKE_PREFIX_PATH"):
            onnx_lib_dir = os.path.join(os.environ.get("CMAKE_PREFIX_PATH"), "lib")
            if os.path.exists(onnx_lib_dir):
                bin_dir = os.path.join(self.install_folder, "bin")
                os.makedirs(bin_dir, exist_ok=True)

                # Copy dylibs for macOS (skip .dSYM directories)
                for dylib in glob.glob(os.path.join(onnx_lib_dir, "*.dylib*")):
                    if os.path.isfile(dylib):  # Skip directories like .dSYM
                        self.output.info(f"Copying {dylib} to {bin_dir}")
                        shutil.copy2(dylib, bin_dir)

                # Copy .so for Linux
                for so in glob.glob(os.path.join(onnx_lib_dir, "*.so*")):
                    if os.path.isfile(so):
                        self.output.info(f"Copying {so} to {bin_dir}")
                        shutil.copy2(so, bin_dir)

    def test(self):
        if not tools.cross_building(self.settings):
            # Set library path to find onnxruntime at runtime
            env_vars = {}
            if os.environ.get("CMAKE_PREFIX_PATH"):
                onnx_lib_path = os.path.join(os.environ.get("CMAKE_PREFIX_PATH"), "lib")
                if self.settings.os == "Macos":
                    env_vars["DYLD_LIBRARY_PATH"] = onnx_lib_path
                else:
                    env_vars["LD_LIBRARY_PATH"] = onnx_lib_path

            with tools.environment_append(env_vars):
                self.run("cd bin && .%stest_silero_vad" % os.sep)
