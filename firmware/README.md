# Firmware

ESP32-based RTU firmware for real-time grid monitoring.

## Overview

The firmware runs on an ESP32 and performs:
- High-speed ADC sampling
- RMS voltage calculation
- Frequency estimation
- DNP3 outstation telemetry

## Files

| File                    | Purpose |
|-------------------------|---------|
| `esp32_rtu_main.ino`    | Main program |
| `adc_sampling.*`        | ADC configuration and sampling |
| `rms.*`                 | RMS calculation |
| `frequency.*`           | Zero-crossing / frequency estimation |
| `dnp3_stub.*`           | DNP3 communication stub |
| `config.h`              | User-configurable settings |
| `utils.h`               | Helper functions |

## Getting Started

### Recommended Toolchain
**PlatformIO** (strongly recommended) or Arduino IDE.

### Setup
1. Clone or open the project.
2. Edit `config.h`:
   - Wi-Fi credentials (if using Wi-Fi)
   - DNP3 master address and local address
   - Sampling parameters
3. Build and flash to ESP32.

### Serial Output
The firmware prints VRMS and frequency to the serial monitor at 115200 baud for easy debugging.

## Configuration (`config.h`)

Key parameters you can adjust:
- `SAMPLE_RATE`
- `SAMPLES_PER_CYCLE`
- DNP3 settings
- Pin assignments

## Notes

- Currently implements a basic DNP3 stub. Full outstation functionality is in progress.
- Designed for both single-channel (SISO) and three-phase (MIMO) hardware.

Further technical details are available in the [dissertation](../docs/RTU_SCADA_WindFarm_Dissertation_Public.pdf.pdf).
