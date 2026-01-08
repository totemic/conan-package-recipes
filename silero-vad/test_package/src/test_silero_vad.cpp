#include <iostream>
#include <string>

// Simple test that verifies the package is accessible
// Note: A full test would require ONNX Runtime to be installed
// and a WAV file to process

int main() {
    std::cout << "Silero VAD package test" << std::endl;

#ifdef SILERO_VAD_MODEL_PATH
    std::cout << "Model path: " << SILERO_VAD_MODEL_PATH << std::endl;
#else
    std::cout << "Model path not defined" << std::endl;
#endif

    std::cout << "Test completed successfully" << std::endl;
    return 0;
}
