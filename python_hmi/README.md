# Python HMI

Human-Machine Interface for the ESP32 RTU.

## Current Status

This folder is under active development. The goal is a clean, cross-platform desktop application for real-time monitoring and configuration of the RTU.

## Planned Features

- Real-time display of voltage, current, frequency, and RMS values
- Trending / historical charts
- DNP3 client to poll the RTU
- Alarm and event logging
- Configuration interface
- Data export (CSV)

## Recommended Stack

- **PySide6** or **Dear PyGui** (lightweight)
- `pydnp3` or similar for DNP3 communication
- Plotly / Matplotlib for charting

## Setup (when code is added)

```bash
cd python_hmi
pip install -r requirements.txt
python main.py
