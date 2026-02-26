from conan import ConanFile
from conan.tools.meson import Meson, MesonToolchain
from conan.tools.layout import basic_layout
from conan.tools.files import get, copy, rmdir
from conan.tools.gnu import PkgConfigDeps
import os

class WebRTCAPMConan(ConanFile):
    name = "webrtc-apm"
    version = "2.1"
    license = "BSD-3-Clause"
    url = "https://gitlab.freedesktop.org/pulseaudio/webrtc-audio-processing"
    description = "WebRTC Audio Processing Module (APM) - includes AGC2, NS, AEC3, VAD (based on WebRTC M131)"
    topics = ("audio", "processing", "webrtc", "agc", "aec", "vad")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    exports_sources = "patches/*"

    def layout(self):
        basic_layout(self, src_folder="src")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("abseil/20240722.0")  # WebRTC APM 2.1 requires Abseil >= 20240722

    def build_requirements(self):
        self.tool_requires("meson/1.2.2")
        self.tool_requires("pkgconf/2.0.3")

    def source(self):
        # Download webrtc-audio-processing 2.1 source (latest, based on WebRTC M131)
        # Version 2.x includes latest improvements and bug fixes from WebRTC project
        get(self,
            "https://gitlab.freedesktop.org/pulseaudio/webrtc-audio-processing/-/archive/v2.1/webrtc-audio-processing-v2.1.tar.gz",
            strip_root=True)

    def generate(self):
        tc = MesonToolchain(self)
        tc.generate()

        deps = PkgConfigDeps(self)
        deps.generate()

    def build(self):
        meson = Meson(self)
        meson.configure()
        meson.build()

    def package(self):
        meson = Meson(self)
        meson.install()

        # Copy license
        copy(self, "COPYING",
             src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))

        # Remove unnecessary files
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # Main library (version 2.x uses libwebrtc-audio-processing-2.a)
        self.cpp_info.libs = ["webrtc-audio-processing-2"]

        # Include paths (version 2.x uses webrtc-audio-processing-2 directory)
        self.cpp_info.includedirs = ["include/webrtc-audio-processing-2"]

        # Set pkg-config name
        self.cpp_info.set_property("pkg_config_name", "webrtc-audio-processing-2")

        # System libs
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread", "m"]
