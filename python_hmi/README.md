# Python SCADA HMI Dashboard

Full-featured Human-Machine Interface for the MIMO Grid Monitoring RTU.

This is the same SCADA HMI shown in **Figure 4.10** of the dissertation (Appendix E).

## Features

- Real-time display of three-phase RMS voltages and currents
- Frequency, THD, phase angle, and power measurements
- Reconstructed three-phase voltage waveform
- Alarm status with colour-coded indicators
- PDS / Grid Code compliance monitoring
- Live DNP3 IEEE 1815 frame inspector (raw bytes)
- Automatic serial reconnection

## Requirements

- Python 3.8 or higher
- ESP32/Feather sending serial telemetry at **115200 baud**

### Install Dependencies

```bash
cd python_hmi
pip install -r requirements.txt
