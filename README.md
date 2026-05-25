# Grid Monitoring RTU & SCADA for Wind Farms

**Low-cost ESP32-based SCADA RTU proxy with DNP3 telemetry, advanced signal conditioning, and Python HMI.**

A complete open-source hardware + firmware + software solution for monitoring grid parameters in wind farm applications. Designed for affordability, real-time performance, and industrial protocol compatibility (DNP3).

<p align="center">
  <img src="images/SCADA_Dashboard.png" width="800" alt="SCADA Dashboard">
</p>

---

## ✨ Features

- **ESP32-based RTU** with high-speed ADC sampling, RMS calculation, frequency measurement, and phase analysis.
- **DNP3 Outstation** support for standard SCADA communication.
- **Custom signal conditioning** hardware for safe grid voltage/current interfacing (including LCL filter modeling).
- **Python HMI** for real-time visualization, trending, alarms, and configuration.
- **Prototypes**: Single-channel SISO and three-phase MIMO builds.
- **Simulation & Modeling**: LTSpice models for system validation.
- **Low-cost focus**: Suitable for educational, research, and small-scale deployments.

---

## 📁 Project Structure

| Folder              | Content |
|---------------------|---------|
| `/firmware`         | ESP32 Arduino code (ADC, RMS, frequency, DNP3) |
| `/hardware`         | Schematics, PCB designs, BOM |
| `/python_hmi`       | Python-based Human-Machine Interface |
| `/ltspice`          | Simulation models (MIMO + LCL) |
| `/docs`             | Dissertation, additional documentation |
| `/images`           | Screenshots and build photos |

---

## 🛠 Quick Start

### Hardware
1. Build the signal conditioning board (see `/hardware` and dissertation for schematics).
2. Assemble the ESP32 prototype (stripboard versions available for SISO and MIMO).
3. Connect CT/PT sensors safely to the grid/wind turbine output.

**⚠️ Safety Note**: High voltage work requires proper isolation, qualified personnel, and adherence to electrical safety standards.

### Firmware
1. Open the project in Arduino IDE or **PlatformIO** (recommended).
2. Configure Wi-Fi / Ethernet and DNP3 settings in `config.h`.
3. Flash to ESP32.
4. Verify telemetry via serial monitor or DNP3 master.

### Python HMI
(See `/python_hmi` folder for setup instructions once populated.)

---

## 📊 Architecture Overview

The system acts as an **RTU proxy** between the physical grid/wind turbine sensors and a central SCADA master.

**Key Components**:
- **Analog Front-End**: Signal conditioning (scaling, filtering, protection) for 3-phase voltage/current.
- **ESP32 RTU**: Samples signals → computes RMS, frequency, power metrics → serves data via DNP3.
- **Communication**: DNP3 over TCP/IP (primary), with potential Modbus fallback.
- **HMI**: Python application for local/remote monitoring and control.
- **Modeling**: LTSpice used to validate MIMO + LCL filter behavior.

(Insert architecture diagram here — e.g., a block diagram exported from your dissertation.)

---

## 📸 Hardware Implementation

### Single-Channel SISO Prototype
<p align="center">
  <img src="images/SISO_Stripboard_Build.jpg" width="700" alt="Single Channel Prototype">
</p>

### Three-Phase MIMO Prototype
<p align="center">
  <img src="images/MIMO_Stripboard_Build.jpg" width="700" alt="Three Phase Prototype">
</p>

---

## 🔬 Signal Conditioning Design

### Conditioning Circuit
<p align="center">
  <img src="images/Single_Channel_Conditioning_Circuit.png" width="900" alt="Conditioning Circuit">
</p>

### Frequency Response (Bode Plot)
<p align="center">
  <img src="images/Bode_Plot.png" width="900" alt="Bode Plot">
</p>

---

## 🔧 Three-Phase System Modelling

### MIMO + LCL System Schematic
<p align="center">
  <img src="images/LCL_Filter_MIMO_Conditioning_Circuit_LTSpice.png" width="1000" alt="LTSpice Schematic">
</p>

### ADC-Ready Three-Phase Voltage Traces
<p align="center">
  <img src="images/Three_Phase_V_to_ADC_Output.png" width="900" alt="Three Phase Traces">
</p>

---

## 📚 Documentation

- **Full Dissertation**: [`docs/RTU_SCADA_WindFarm_Dissertation_Public.pdf`](docs/RTU_SCADA_WindFarm_Dissertation_Public.pdf) — Detailed design, methodology, results, and analysis.
- Hardware schematics and BOM (in `/hardware`)
- Firmware documentation (in `/firmware`)
- HMI guide (in `/python_hmi`)

---

## 🚀 Roadmap / Future Work

- Complete and expand the Python HMI with real-time charting and DNP3 client.
- Add more robust error handling and logging in firmware.
- PCB design (move beyond stripboard).
- Multi-RTU wind farm simulation.
- Security hardening (authentication, encryption for DNP3).
- Field testing on actual wind turbine or lab microgrid.

---

## 🧪 Results & Performance

(Extract key results from your dissertation, e.g.:
- Sampling rate achieved: XX kHz
- RMS accuracy: ±X%
- DNP3 polling latency: XX ms
- Total system cost: ~$XX)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- Dissertation supervisor / university (add if desired)
- Open-source libraries used (DNP3, Arduino, etc.)

---

**Contributions welcome!** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Built as part of [Your Name]’s academic / research work on low-cost renewable energy monitoring systems.*
