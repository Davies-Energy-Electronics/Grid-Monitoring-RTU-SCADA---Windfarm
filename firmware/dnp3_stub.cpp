#include <Arduino.h>
#include "dnp3_stub.h"

void setupDNP3()
{
    Serial.println("DNP3 Interface Initialized");
}

void sendTelemetry(float vrms, float frequency)
{
    Serial.print("Sending DNP3 Telemetry -> ");

    Serial.print("VRMS: ");
    Serial.print(vrms);

    Serial.print(" Frequency: ");
    Serial.println(frequency);
}
