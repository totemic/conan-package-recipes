# WebRTC AGC Conan Package

Conan package for [WebRTC_AGC](https://github.com/cpuimage/WebRTC_AGC) - a standalone port of WebRTC's Automatic Gain Control (AGC) module written in C.

## Features

- Automatic gain control for audio streams
- Dynamic level adjustment
- Compression gain control
- Optional limiter
- Pure C implementation
- Cross-platform support

## Package Information

- **License**: BSD-3-Clause
- **Version**: 1.0
- **Topics**: audio, agc, webrtc, automatic-gain-control, voice

## Usage

### Add to conanfile.txt

```ini
[requires]
webrtc-agc/1.0

[generators]
cmake
```

### Add to conanfile.py

```python
class YourProject(ConanFile):
    requires = "webrtc-agc/1.0"
```

### Example Code

```c
#include "agc.h"
#include <stdio.h>

int main() {
    // Create AGC instance
    void* agc_handle = WebRtcAgc_Create();

    // Initialize AGC (minLevel=0, maxLevel=255, agcMode=0)
    WebRtcAgc_Init(agc_handle, 0, 255, 0);

    // Configure AGC
    WebRtcAgcConfig config;
    config.targetLevelDbfs = 3;      // Target level in dBfs (0-31)
    config.compressionGaindB = 9;    // Compression gain in dB (0-90)
    config.limiterEnable = 1;        // Enable limiter
    WebRtcAgc_set_config(agc_handle, config);

    // Process audio
    short audio_in[160];   // 10ms at 16kHz
    short audio_out[160];
    int micLevelIn = 100;
    int micLevelOut = 0;
    unsigned char saturationWarning = 0;

    WebRtcAgc_Process(
        agc_handle,
        (const short* const*)&audio_in,
        1,              // num_bands
        160,            // samples
        (short* const*)&audio_out,
        micLevelIn,
        &micLevelOut,
        0,              // echo
        &saturationWarning
    );

    // Clean up
    WebRtcAgc_Free(agc_handle);

    return 0;
}
```

## Building the Package

### Local Build

```bash
cd webrtc-agc
conan create . webrtc-agc/1.0@
```

### With Options

```bash
# Build as shared library
conan create . webrtc-agc/1.0@ -o shared=True

# Specific build type
conan create . webrtc-agc/1.0@ -s build_type=Release
```

## Package Options

| Option | Default | Description |
|--------|---------|-------------|
| shared | False   | Build as shared library |
| fPIC   | True    | Position independent code (not available on Windows) |

## API Reference

### Core Functions

- `WebRtcAgc_Create()` - Create AGC instance
- `WebRtcAgc_Free()` - Free AGC instance
- `WebRtcAgc_Init()` - Initialize AGC
- `WebRtcAgc_Process()` - Process audio samples
- `WebRtcAgc_set_config()` - Set AGC configuration
- `WebRtcAgc_get_config()` - Get current configuration

### Configuration Parameters

**WebRtcAgcConfig** structure:
- `targetLevelDbfs` - Target RMS level in dBfs (0-31, typical: 3)
- `compressionGaindB` - Gain applied to input (0-90, typical: 9)
- `limiterEnable` - Enable/disable limiter (0 or 1)

## Cross-Compilation

Similar to libfvad, you can use conan profiles for cross-compilation:

```bash
# ARM cross-compilation example
conan create . webrtc-agc/1.0@ --profile=armv8-profile
```

## Testing

The test package verifies:
- AGC instance creation and initialization
- Configuration setting and retrieval
- Audio processing with dummy data
- Proper cleanup

Run tests:
```bash
conan create . webrtc-agc/1.0@
```

## Notes

- The library is built from the master branch of the upstream repository
- For production use, consider pinning to a specific commit hash in conanfile.py
- Audio samples should be provided in 10ms frames for best results
- Sample rate support: 8kHz, 16kHz, 32kHz, 48kHz (depending on configuration)

## Troubleshooting

### Build Issues

If you encounter build issues, ensure:
1. CMake version >= 3.9 is installed
2. A compatible C compiler is available
3. Conan is properly configured for your platform

### Runtime Issues

- Check that audio buffer sizes match expected frame length (typically 10ms)
- Verify sample rate matches AGC configuration
- Ensure mic levels are in valid range (0-255)

## Related Packages

- **libfvad** - Voice Activity Detection
- **silero-vad** - Neural network-based VAD
- **libebur128** - EBU R128 loudness measurement

## License

This package follows the BSD-3-Clause license of the upstream project.
