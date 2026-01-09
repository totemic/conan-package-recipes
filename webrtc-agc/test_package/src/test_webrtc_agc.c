#include "agc.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    printf("Testing WebRTC AGC library...\n");

    // Create AGC instance
    void* agc_handle = WebRtcAgc_Create();
    if (!agc_handle) {
        fprintf(stderr, "ERROR: Failed to create AGC instance\n");
        return 1;
    }
    printf("✓ AGC instance created successfully\n");

    // Initialize AGC
    // Parameters: handle, minLevel (0), maxLevel (255), agcMode (0=unchanged), fs (sample rate)
    const int sample_rate = 16000;  // 16 kHz
    int result = WebRtcAgc_Init(agc_handle, 0, 255, 0, sample_rate);
    if (result != 0) {
        fprintf(stderr, "ERROR: Failed to initialize AGC (error code: %d)\n", result);
        WebRtcAgc_Free(agc_handle);
        return 1;
    }
    printf("✓ AGC initialized successfully\n");

    // Configure AGC
    WebRtcAgcConfig config;
    config.targetLevelDbfs = 3;      // Target level in dBfs (0-31)
    config.compressionGaindB = 9;    // Compression gain in dB (0-90)
    config.limiterEnable = 1;        // Enable limiter

    result = WebRtcAgc_set_config(agc_handle, config);
    if (result != 0) {
        fprintf(stderr, "ERROR: Failed to set AGC config (error code: %d)\n", result);
        WebRtcAgc_Free(agc_handle);
        return 1;
    }
    printf("✓ AGC configuration set successfully\n");

    // Verify configuration
    WebRtcAgcConfig retrieved_config;
    result = WebRtcAgc_get_config(agc_handle, &retrieved_config);
    if (result != 0) {
        fprintf(stderr, "ERROR: Failed to get AGC config (error code: %d)\n", result);
        WebRtcAgc_Free(agc_handle);
        return 1;
    }
    printf("✓ AGC configuration retrieved successfully\n");
    printf("  Target Level: %d dBfs\n", retrieved_config.targetLevelDbfs);
    printf("  Compression Gain: %d dB\n", retrieved_config.compressionGaindB);
    printf("  Limiter: %s\n", retrieved_config.limiterEnable ? "enabled" : "disabled");

    // Test with dummy audio data
    const int samples = 160;        // 10ms at 16kHz
    short audio_in[160];
    short audio_out[160];

    // Generate some dummy audio (sine-like pattern)
    for (int i = 0; i < samples; i++) {
        audio_in[i] = (short)(1000 * (i % 100) / 100.0);
    }

    // Process audio
    int micLevelIn = 0;  // Input microphone level (0-255)
    int micLevelOut = 0;
    unsigned char saturationWarning = 0;

    // WebRtcAgc_Process expects pointers to pointers for audio buffers
    const short* audio_in_ptr = audio_in;
    short* audio_out_ptr = audio_out;

    result = WebRtcAgc_Process(
        agc_handle,
        (const short* const*)&audio_in_ptr,
        1,                      // num_bands
        samples,
        (short* const*)&audio_out_ptr,
        micLevelIn,
        &micLevelOut,
        0,                      // echo
        &saturationWarning
    );

    if (result != 0) {
        fprintf(stderr, "ERROR: Failed to process audio (error code: %d)\n", result);
        WebRtcAgc_Free(agc_handle);
        return 1;
    }
    printf("✓ Audio processing successful\n");
    printf("  Input mic level: %d\n", micLevelIn);
    printf("  Output mic level: %d\n", micLevelOut);
    printf("  Saturation warning: %s\n", saturationWarning ? "yes" : "no");

    // Clean up
    WebRtcAgc_Free(agc_handle);
    printf("✓ AGC instance freed successfully\n");

    printf("\n✓ All tests passed!\n");
    return 0;
}
