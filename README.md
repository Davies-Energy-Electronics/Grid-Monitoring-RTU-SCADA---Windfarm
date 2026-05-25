# Grid Monitoring RTU & SCADA – Wind Farm Application

Low-cost ESP32-based Remote Terminal Unit (RTU) with DNP3 support, custom signal conditioning hardware, and Python HMI for grid parameter monitoring in wind energy systems.

## Overview

This project implements an affordable monitoring solution for wind farm grid connection points. The system acquires three-phase voltage and current signals, performs real-time RMS and frequency calculations on an ESP32, and exposes the data via DNP3 to a SCADA master. A companion Python HMI provides local visualisation, trending, and configuration.

The design includes both single-channel (SISO) and three-phase (MIMO) prototypes, supported by LTSpice modelling and full documentation.

## Project Structure

- **`/firmware`** – ESP32 code (ADC sampling, RMS, frequency measurement, DNP3 outstation)
- **`/hardware`** – Schematics, BOM, and build information
- **`/python_hmi`** – Python-based Human Machine Interface
- **`/ltspice`** – Simulation models (MIMO system + LCL filter)
- **`/docs`** – Dissertation and supporting documents
- **`/images`** – Photos and diagrams

## Key Features

- High-speed ADC sampling and real-time signal processing on ESP32
- DNP3 protocol support for SCADA integration
- Custom analogue front-end with scaling, filtering and protection
- Python HMI for real-time display and data logging
- Comprehensive documentation including modelling and experimental results

## Getting Started

### Hardware
Refer to the schematics and photos in `/hardware`. Prototypes were built on stripboard for both SISO and MIMO versions. Proper isolation and safety precautions are essential when interfacing with grid voltages.

### Firmware
Open the project in Arduino IDE or PlatformIO (recommended), configure Wi-Fi/Ethernet and DNP3 settings, then flash to the ESP32. Detailed instructions are in the `/firmware` folder.

### Python HMI
Under active development. See `/python_hmi` for current status and setup.

## Documentation

Full technical details, design methodology, test results and analysis are in the dissertation:

[**RTU_SCADA_WindFarm_Dissertation_Public.pdf**](docs/RTU_SCADA_WindFarm_Dissertation_Public.pdf.pdf)

## Gallery

**Three-Phase MIMO Prototype**  
![MIMO Build](images/MIMO_Stripboard_Build.jpg)

**Signal Conditioning Circuit**  
![Conditioning Circuit](images/Single_Channel_Conditioning_Circuit.png)

**LTSpice Model**  
![LTSpice Schematic](images/LCL_Filter_MIMO_Conditioning_Circuit_LTSpice.png)

**Example Three-Phase Output**  
![Three Phase Traces](images/Three_Phase_V_to_ADC_Output.png)

## Results & Performance

Key results (sampling rates, accuracy figures, system cost, etc.) are detailed in the dissertation.

## Future Work

- Complete the Python HMI with live trending and alarms
- Migrate to proper PCBs
- Add Modbus support
- Enhance security and multi-RTU coordination
- Field testing on a microgrid or small wind turbine

## Acknowledgements

Developed by **Jack Davies** under the supervision of **Dr Lei Kang**.

## License

MIT License. See the [LICENSE](LICENSE) file for details.

---

Contributions and suggestions are welcome.
