# Grid Monitoring RTU & SCADA – Wind Farm Application

Low-cost ESP32-based Remote Terminal Unit with DNP3 support, custom signal conditioning hardware, and a full Python SCADA HMI for real-time grid monitoring in wind energy systems.

## Overview

This project delivers an end-to-end, affordable monitoring solution for wind farm grid connection points. It acquires three-phase voltage and current signals, performs real-time RMS, frequency, THD and power calculations on an ESP32, and transmits data using DNP3. A complete Python HMI provides live visualisation, alarms, waveform reconstruction, and compliance monitoring.

Developed as final-year dissertation work under the supervision of **Dr Lei Kang**.

## Key Features

- High-speed ADC sampling and real-time processing on ESP32
- DNP3 IEEE 1815 outstation implementation
- Custom analogue signal conditioning with protection and filtering
- Full Python SCADA HMI (live waveform + alarms + compliance)
- Single-channel (SISO) and three-phase (MIMO) prototypes
- Detailed LTSpice modelling and validation

## Results & Performance

(Add your key numbers here from the dissertation)

- Sampling rate: XX kS/s
- RMS voltage accuracy: ±X.X%
- Frequency accuracy: ±0.X Hz
- Successful real-time DNP3 telemetry transmission
- Total prototype cost: ~£XX

## Project Structure

- **`/firmware`** – ESP32 code (ADC, RMS, frequency, DNP3)
- **`/hardware`** – Schematics, BOM, build photos
- **`/python_hmi`** – Complete SCADA HMI dashboard
- **`/ltspice`** – Simulation models
- **`/docs`** – Full dissertation
- **`/images`** – Photos and diagrams

## Getting Started

### Hardware
See `/hardware` folder for schematics and photos. Prototypes were built on stripboard. **High voltage safety precautions are essential.**

### Firmware
Open in Arduino IDE or PlatformIO, configure `config.h`, and flash to ESP32.

### Python HMI
```bash
cd python_hmi
pip install pyserial
python SCADA_HMI.py
