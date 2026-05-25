"""
Grid Monitoring RTU - Python HMI
Basic GUI Skeleton
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGroupBox, QPushButton, QGridLayout
)
from PySide6.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np


class GridHMI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wind Farm Grid Monitor - RTU HMI")
        self.setMinimumSize(1200, 700)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # === Left Panel: Real-time Values ===
        left_panel = QVBoxLayout()
        
        title = QLabel("Grid Parameters")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_panel.addWidget(title)

        # Voltage, Current, Frequency boxes
        self.voltage_label = self.create_value_box("Voltage (RMS)", "0.00", "V")
        self.current_label = self.create_value_box("Current (RMS)", "0.00", "A")
        self.freq_label    = self.create_value_box("Frequency", "50.00", "Hz")
        self.power_label   = self.create_value_box("Active Power", "0.00", "kW")

        left_panel.addWidget(self.voltage_label)
        left_panel.addWidget(self.current_label)
        left_panel.addWidget(self.freq_label)
        left_panel.addWidget(self.power_label)

        # Connection status
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        left_panel.addWidget(self.status_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect to RTU")
        self.connect_btn.clicked.connect(self.toggle_connection)
        btn_layout.addWidget(self.connect_btn)
        
        left_panel.addLayout(btn_layout)
        left_panel.addStretch()

        # === Right Panel: Charts ===
        right_panel = QVBoxLayout()
        
        # Real-time plot
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setTitle("Voltage Waveform (Last 2 seconds)")
        self.plot_widget.setLabel('left', 'Voltage', 'V')
        self.plot_widget.setLabel('bottom', 'Time', 's')
        self.curve = self.plot_widget.plot(pen=pg.mkPen(color='b', width=2))
        
        right_panel.addWidget(self.plot_widget)

        # Combine panels
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        # Dummy data timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dummy_data)
        self.timer.start(500)  # update every 500ms

        self.is_connected = False
        self.time_data = []
        self.voltage_data = []

    def create_value_box(self, title: str, value: str, unit: str):
        box = QGroupBox(title)
        layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #0066cc;")
        unit_label = QLabel(unit)
        unit_label.setStyleSheet("font-size: 14px;")
        
        layout.addWidget(value_label)
        layout.addWidget(unit_label)
        box.setLayout(layout)
        return box

    def toggle_connection(self):
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.status_label.setText("Status: Connected")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.connect_btn.setText("Disconnect")
        else:
            self.status_label.setText("Status: Disconnected")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setText("Connect to RTU")

    def update_dummy_data(self):
        """Replace this later with real data from ESP32"""
        # Simulate values
        v = 230 + np.random.normal(0, 2)
        i = 15 + np.random.normal(0, 0.5)
        f = 49.9 + np.random.normal(0, 0.05)

        # Update text
        self.voltage_label.findChild(QLabel).setText(f"{v:.2f}")
        self.current_label.findChild(QLabel).setText(f"{i:.2f}")
        self.freq_label.findChild(QLabel).setText(f"{f:.2f}")

        # Update plot
        self.time_data.append(len(self.time_data) * 0.1)
        self.voltage_data.append(v)
        
        if len(self.time_data) > 200:
            self.time_data.pop(0)
            self.voltage_data.pop(0)
        
        self.curve.setData(self.time_data, self.voltage_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GridHMI()
    window.show()
    sys.exit(app.exec())
