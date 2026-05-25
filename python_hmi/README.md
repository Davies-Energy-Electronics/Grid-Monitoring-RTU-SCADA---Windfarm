# Python SCADA HMI

Full-featured Human-Machine Interface for the MIMO RTU.

## Features

- Reads live telemetry from the ESP32/Feather via USB-Serial (115200 baud)
- Displays all RMS voltages & currents, frequencies, THD, phase angles and power quantities
- Real-time three-phase waveform reconstruction
- Alarm status with colour coding
- PDS / Grid Code compliance indicators
- Live DNP3 frame inspector (raw bytes)

This is the same dashboard shown in **Figure 4.10** of the dissertation.

## How to Run

1. Connect the ESP32/Feather to your PC via USB.
2. **Close the Arduino Serial Monitor** (important — only one program can use the port).
3. Run the HMI:

```bash
cd python_hmi
pip install pyserial
python SCADA_HMI.py
