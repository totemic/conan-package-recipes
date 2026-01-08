#include <stdio.h>
#include <stdlib.h>
#include <ebur128.h>

int main() {
    ebur128_state* st = NULL;
    
    printf("Testing libebur128 v%d.%d.%d\n", 
           EBUR128_VERSION_MAJOR, EBUR128_VERSION_MINOR, EBUR128_VERSION_PATCH);
    
    // Create state for 48kHz, mono audio
    st = ebur128_init(1, 48000, EBUR128_MODE_I);
    if (!st) {
        printf("Failed to initialize ebur128 state\n");
        return 1;
    }
    
    printf("Successfully initialized libebur128 state\n");
    
    // Generate some test samples (silence)
    double samples[480] = {0}; // 10ms of silence at 48kHz
    
    // Add samples to the state
    int err = ebur128_add_frames_double(st, samples, 480);
    if (err != EBUR128_SUCCESS) {
        printf("Failed to add frames: error %d\n", err);
        ebur128_destroy(&st);
        return 1;
    }
    
    // Get loudness measurement
    double loudness;
    err = ebur128_loudness_global(st, &loudness);
    if (err != EBUR128_SUCCESS) {
        printf("Failed to get loudness: error %d\n", err);
    } else {
        printf("Measured loudness: %.2f LUFS\n", loudness);
    }
    
    ebur128_destroy(&st);
    printf("libebur128 test passed!\n");
    return 0;
}