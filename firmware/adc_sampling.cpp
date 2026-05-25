#include <Arduino.h>
#include "config.h"
#include "adc_sampling.h"

void setupADC()
{
    analogReadResolution(12);
}

void collectSamples(float *buffer, int length)
{
    int sampleDelay = 1000000 / SAMPLE_RATE;

    for (int i = 0; i < length; i++)
    {
        int raw = analogRead(ADC_PIN);

        float voltage = (raw / ADC_RESOLUTION) * ADC_REFERENCE;

        voltage -= ADC_BIAS;

        buffer[i] = voltage;

        delayMicroseconds(sampleDelay);
    }
}
