#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class OnnxRuntimeConan(ConanFile):
    name = "onnxruntime"
    version = "1.19.2"
    settings = "os", "compiler", "build_type", "arch"
    topics = ("ml", "onnx", "inference", "neural-network")
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    homepage = "https://onnxruntime.ai/"
    url = "https://github.com/microsoft/onnxruntime"
    license = "MIT"
    description = "ONNX Runtime: cross-platform, high performance ML inferencing and training accelerator"
    # no_copy_source = True  # Disabled to prevent source contamination between macOS/Linux builds

    def configure(self):
        # ONNX Runtime pre-built binaries are always shared libraries
        self.options.shared = True

    def source(self):
        """Extract pre-built ONNX Runtime binaries for the target platform"""
        # Determine the correct package based on OS and architecture
        if self.settings.os == "Macos":
            if self.settings.arch == "x86_64":
                filename = "onnxruntime-osx-x86_64-{}.tgz".format(self.version)
            else:
                raise Exception("Unsupported macOS architecture: {}".format(self.settings.arch))
        elif self.settings.os == "Linux":
            if self.settings.arch == "x86_64":
                filename = "onnxruntime-linux-x64-{}.tgz".format(self.version)
            elif self.settings.arch == "armv8":
                filename = "onnxruntime-linux-aarch64-{}.tgz".format(self.version)
            else:
                raise Exception("Unsupported Linux architecture: {}".format(self.settings.arch))
        else:
            raise Exception("Unsupported OS: {}".format(self.settings.os))

        # For local development: use local tarballs if available
        # For CI/CD: download from GitHub releases
        local_tarball = os.path.expanduser("~/koko/third-party/{}".format(filename))

        if os.path.exists(local_tarball):
            self.output.info("Using local ONNX Runtime tarball: {}".format(local_tarball))
            tools.unzip(local_tarball, destination=self.source_folder)
        else:
            # Download from GitHub releases
            base_url = "https://github.com/microsoft/onnxruntime/releases/download/v{}/".format(self.version)
            url = base_url + filename
            self.output.info("Downloading ONNX Runtime from {}".format(url))
            tools.get(url)

    def build(self):
        # Pre-built binaries, no build needed
        pass

    def package(self):
        # Find the extracted directory (it will have a prefix like onnxruntime-osx-x86_64-1.19.2)
        extracted_dirs = [d for d in os.listdir(self.source_folder) if d.startswith("onnxruntime-")]
        if not extracted_dirs:
            raise Exception("Could not find extracted ONNX Runtime directory")

        source_dir = os.path.join(self.source_folder, extracted_dirs[0])

        # Copy headers
        self.copy("*.h", dst="include", src=os.path.join(source_dir, "include"), keep_path=False)

        # Copy libraries (excluding .dSYM debug symbols)
        lib_src = os.path.join(source_dir, "lib")
        lib_dst = os.path.join(self.package_folder, "lib")
        os.makedirs(lib_dst, exist_ok=True)

        for item in os.listdir(lib_src):
            item_path = os.path.join(lib_src, item)
            # Skip .dSYM directories
            if item.endswith(".dSYM") or os.path.isdir(item_path):
                continue
            # Copy dylib files and symlinks
            if item.endswith(".dylib") or ".dylib." in item or item.endswith(".so") or ".so." in item:
                if os.path.islink(item_path):
                    # Copy symlink
                    linkto = os.readlink(item_path)
                    os.symlink(linkto, os.path.join(lib_dst, item))
                else:
                    # Copy actual file
                    self.copy(item, dst="lib", src=lib_src, keep_path=False)

        # Copy Windows libraries if present
        self.copy("*.dll", dst="bin", src=lib_src, keep_path=False)
        self.copy("*.lib", dst="lib", src=lib_src, keep_path=False)

        # Copy license
        self.copy("LICENSE", dst="licenses", src=source_dir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["onnxruntime"]
        self.cpp_info.names["cmake_find_package"] = "onnxruntime"
        self.cpp_info.names["cmake_find_package_multi"] = "onnxruntime"

        # Set RPATH for runtime library loading
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-Wl,-rpath,@loader_path")
            self.cpp_info.exelinkflags.append("-Wl,-rpath,@executable_path")
            # Also add the package lib directory
            lib_path = os.path.join(self.package_folder, "lib")
            self.cpp_info.exelinkflags.append("-Wl,-rpath,{}".format(lib_path))
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
            self.cpp_info.system_libs.append("dl")
            self.cpp_info.exelinkflags.append("-Wl,-rpath,$ORIGIN")
            lib_path = os.path.join(self.package_folder, "lib")
            self.cpp_info.exelinkflags.append("-Wl,-rpath,{}".format(lib_path))
