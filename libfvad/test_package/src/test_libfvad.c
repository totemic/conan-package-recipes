#include <stdio.h>
#include <fvad.h>

int main() {
    Fvad *vad = fvad_new();
    if (vad == NULL) {
        printf("Failed to create VAD instance\n");
        return 1;
    }
    
    if (fvad_set_mode(vad, 0) < 0) {
        printf("Failed to set VAD mode\n");
        fvad_free(vad);
        return 1;
    }
    
    if (fvad_set_sample_rate(vad, 16000) < 0) {
        printf("Failed to set sample rate\n");
        fvad_free(vad);
        return 1;
    }
    
    printf("libfvad test passed - VAD instance created and configured successfully\n");
    
    fvad_free(vad);
    return 0;
}