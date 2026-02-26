# WebRTC Audio Processing Module (APM) - Conan Package

This package provides the WebRTC Audio Processing Module (APM) which includes:
- **AGC2** (Automatic Gain Control v2) - Better than standalone agc.h
- **NS** (Noise Suppression)
- **AEC3** (Acoustic Echo Cancellation v3)
- **VAD** (Voice Activity Detection)
- **Transient Suppressor**

## Version

- **webrtc-apm**: 2.1 (based on WebRTC M131, released 2025)
- **Source**: https://gitlab.freedesktop.org/pulseaudio/webrtc-audio-processing
- **Matches**: PulseAudio webrtc-audio-processing 2.1 used in your system

## Building the Package

### Local Build (macOS/Linux)

```bash
cd /Users/ashwin/koko/conan-package-recipes/webrtc-apm

# Create package
conan create . --build=missing

# Or upload to your artifactory
conan create . --build=missing
conan upload webrtc-apm/2.1@totemic/stable -r=totemic-private --all
```

### Cross-compile for ARM64

```bash
# Using your existing ARM Docker setup
tools/arm-ssh.sh conan create /home/conan/repos/conan-package-recipes/webrtc-apm \
    --build=missing \
    --profile:host /home/conan/repos/embedded-sw/conanprofile-armv8-docker.txt \
    --profile:build /home/conan/repos/embedded-sw/conanprofile_build_linux_x86.txt
```

## Using in Your Project

### Update conanfile.txt

Replace:
```
webrtc-agc/1.0@totemic/stable
```

With:
```
webrtc-apm/2.1@totemic/stable
```

### Update CMakeLists.txt

```cmake
find_package(webrtc-apm REQUIRED)
target_link_libraries(guardian PRIVATE webrtc-apm::webrtc-apm)
```

### Update Code

Replace:
```cpp
#include <agc.h>  // Old standalone AGC
```

With:
```cpp
#include "modules/audio_processing/include/audio_processing.h"
```

## Dependencies

- **abseil**: C++ library (required by WebRTC)
- **meson**: Build system
- **pkgconf**: For pkg-config support

## Notes

- This package uses **Meson build system** (same as upstream webrtc-audio-processing)
- Includes the full APM, not just AGC
- Compatible with WebRTC M131+ API
- Thread-safe when used correctly (lock per instance)
