#include <math.h>
#include "rms.h"

float calculateRMS(float *samples, int length)
{
    float sum = 0.0;

    for (int i = 0; i < length; i++)
    {
        sum += samples[i] * samples[i];
    }

    return sqrt(sum / length);
}
