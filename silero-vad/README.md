# Silero VAD Conan Package

This package provides Silero VAD (Voice Activity Detection) - a pre-trained enterprise-grade Voice Activity Detector using ONNX Runtime.

## Features

- Pre-trained VAD model (v5.0)
- ONNX-based inference
- Support for 8000 Hz and 16000 Hz audio
- Header-only C++ interface
- Includes ONNX model file

## Requirements

- ONNX Runtime (must be installed separately or provided via Conan)
- C++17 compatible compiler

## Usage

### In conanfile.txt

```
[requires]
silero-vad/5.0@totemic/stable

[generators]
cmake
```

### In CMakeLists.txt

```cmake
find_package(SileroVAD REQUIRED)
target_link_libraries(your_target SileroVAD::SileroVAD)
```

### In your C++ code

The package includes:
- `wav.h` - WAV file handling utilities
- `silero_vad.onnx` - Pre-trained model file

The model file path is available via the `SILERO_VAD_MODEL_PATH` define.

```cpp
#include <silero-vad/wav.h>
// Use SILERO_VAD_MODEL_PATH to access the model file
```

For complete usage examples, see the [official Silero VAD repository](https://github.com/snakers4/silero-vad/tree/master/examples/cpp).

## Building

```bash
conan create . silero-vad/5.0@totemic/stable
```

## License

MIT License - See the [Silero VAD repository](https://github.com/snakers4/silero-vad) for details.
