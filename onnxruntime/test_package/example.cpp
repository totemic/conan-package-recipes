#include <onnxruntime_cxx_api.h>
#include <iostream>

int main() {
    try {
        Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "test");
        std::cout << "ONNX Runtime initialized successfully!" << std::endl;
        return 0;
    } catch (const Ort::Exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
