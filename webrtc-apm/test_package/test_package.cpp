#include <iostream>
#include "modules/audio_processing/include/audio_processing.h"

int main() {
    // Test that we can create an AudioProcessing instance (version 2.1)
    // Returns rtc::scoped_refptr (WebRTC's reference-counted pointer)
    webrtc::AudioProcessingBuilder builder;
    rtc::scoped_refptr<webrtc::AudioProcessing> apm = builder.Create();

    if (apm) {
        std::cout << "✅ WebRTC AudioProcessing v2.1 created successfully!" << std::endl;
        std::cout << "   Package is ready to use in embedded-sw3 project" << std::endl;
        return 0;
    } else {
        std::cerr << "❌ Failed to create AudioProcessing" << std::endl;
        return 1;
    }
}
