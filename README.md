# ESP32 Grid Monitoring RTU Proxy (Windfarm SCADA)

A low-cost, edge-computing Remote Terminal Unit (RTU) proxy based on the ESP32 architecture. Designed for real-time wind farm substations to bridge physical grid telemetry with master SCADA architectures using the DNP3 protocol.

## System Architecture

The unit leverages the ESP32 dual-core processor to isolate deterministic tasks: Core 0 handles the asynchronous DNP3 outstation stack and network telemetry, while Core 1 performs high-speed ADC sampling, digital filtering, and updates the local HMI.

![System Architecture](images/system_architecture.png)

### Key Specifications
* **Processor:** ESP32 (Dual-Core Xtensa @ 240MHz, integrated Wi-Fi/BLE)
* **Telemetry Protocol:** DNP3 (Distributed Network Protocol v3.0) Level 2 compliant Outstation
* **Sampling Rate:** Configurable up to 4kHz per channel for wave-shape integrity
* **Local Interface:** SPI-driven TFT HMI for real-time hardware diagnostics and metrics

---

## Signal Conditioning & Hardware

To interface the 3.3V single-ended ESP32 internal ADCs with industrial grid instrumentation transformers (CTs and PTs), a custom analog front-end was developed.

![Hardware and Prototype Setup](images/hardware_setup.png)

### Front-End Engineering Features:
* **Galvanic Isolation:** High-transient isolation to protect digital logic from grid surges.
* **Biasing & Scaling:** Active op-amp circuitry providing a precise DC bias offset (+1.65V) and attenuation to match the 0–3.3V input range.
* **Anti-Aliasing:** Active 2nd-order low-pass filters to prevent high-frequency grid noise from aliasing during digital signal processing.

---

## Human Machine Interface (HMI)

The local HMI provides substation technicians with zero-latency physical status verification independent of the upstream SCADA network connection.

![HMI Dashboard](images/hmi_dashboard.png)

### Monitored Grid Metrics:
* **Phase Parameters:** Three-phase AC voltage and current waveforms / RMS calculation.
* **Grid State:** Real-time frequency variations ($\pm 0.01\text{ Hz}$ accuracy) and active power calculations.
* **Network Status:** DNP3 link-layer heartbeat, session states, and transmit/receive fault logs.

---

## Directory Structure

```text
├── docs/               # Technical dissertation and design documentation
├── hardware/           # Schematics, PCB layouts, and analog simulation files
├── hmi/                # Nextion / TFT HMI interface assets and UI codebase
├── src/                # ESP32 firmware source code (DNP3 stack, ADC drivers, DSP)
└── images/             # Documentation visuals
