#include "frequency.h"

float estimateFrequency(
    float *samples,
    int length,
    float sampleRate)
{
    int crossings = 0;

    for (int i = 1; i < length; i++)
    {
        if (samples[i - 1] < 0 && samples[i] >= 0)
        {
            crossings++;
        }
    }

    float duration = (float)length / sampleRate;

    return crossings / duration;
}
