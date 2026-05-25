# Grid Monitoring RTU & SCADA – Wind Farm Application

Low-cost ESP32-based Remote Terminal Unit (RTU) with DNP3 support, custom signal conditioning hardware, and a complete Python SCADA HMI for real-time grid monitoring in wind energy systems.

## Overview

This project implements an end-to-end monitoring solution for wind farm grid connection points. The system acquires three-phase voltage and current signals, performs real-time RMS, frequency, THD and power calculations on an ESP32, and transmits data using the DNP3 (IEEE 1815) protocol. A full-featured Python HMI provides live visualisation, waveform reconstruction, alarms, and compliance monitoring.

Developed by **Jack Davies** under the supervision of **Dr Lei Kang**.

## Key Features

- High-speed ADC sampling and real-time signal processing on ESP32
- DNP3 outstation implementation
- Custom analogue signal conditioning with protection and filtering
- Complete Python SCADA HMI with live three-phase waveform
- Single-channel (SISO) and three-phase (MIMO) prototypes
- LTSpice modelling and validation

## Results & Performance

→ Add your key results from the dissertation here (sampling rate, accuracy, cost, etc.)

## Project Structure

- **`/firmware`** – ESP32 code (ADC, RMS, frequency, DNP3)
- **`/hardware`** – Schematics, BOM, build photos
- **`/python_hmi`** – Complete SCADA HMI dashboard
- **`/ltspice`** – Simulation models
- **`/docs`** – Full dissertation
- **`/images`** – Photos and diagrams

## Getting Started

### Hardware
Refer to `/hardware` for schematics and photos. **High voltage safety precautions required.**

### Firmware
Open in Arduino IDE or PlatformIO, configure `config.h`, and flash to ESP32.

### Python HMI
```bash
cd python_hmi
pip install -r requirements.txt
python SCADA_HMI.py
