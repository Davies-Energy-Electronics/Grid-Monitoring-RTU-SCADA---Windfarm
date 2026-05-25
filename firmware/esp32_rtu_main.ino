#include "config.h"
#include "adc_sampling.h"
#include "rms.h"
#include "frequency.h"
#include "dnp3_stub.h"

float voltageSamples[SAMPLES_PER_CYCLE];

void setup()
{
    Serial.begin(115200);

    setupADC();
    setupDNP3();

    Serial.println("ESP32 RTU Starting...");
}

void loop()
{
    collectSamples(voltageSamples, SAMPLES_PER_CYCLE);

    float vrms = calculateRMS(voltageSamples, SAMPLES_PER_CYCLE);

    float frequency = estimateFrequency(
        voltageSamples,
        SAMPLES_PER_CYCLE,
        SAMPLE_RATE
    );

    Serial.print("VRMS: ");
    Serial.println(vrms);

    Serial.print("Frequency: ");
    Serial.println(frequency);

    sendTelemetry(vrms, frequency);

    delay(100);
