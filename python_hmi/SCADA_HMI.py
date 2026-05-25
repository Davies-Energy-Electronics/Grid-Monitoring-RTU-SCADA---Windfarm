"""
MIMO RTU - SCADA HMI Dashboard
Reads serial telemetry from ESP32/Feather M6 sketch
Displays live measurements, alarms, waveform, and DNP3 frame status

Usage: python SCADA_HMI.py
"""

import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time
import re
import math
import sys


# ── Data Store ─────────────────────────────────────────────────────

class RTUData:
    def __init__(self):
        self.Va_rms = 0.0
        self.Vb_rms = 0.0
        self.Vc_rms = 0.0
        self.Ib_rms = 0.0
        self.Ic_rms = 0.0
        self.f_Va = 0.0
        self.f_Vb = 0.0
        self.f_Vc = 0.0
        self.THD_Va = 0.0
        self.THD_Vb = 0.0
        self.THD_Vc = 0.0
        self.Ph_VbIb = 0.0
        self.Ph_VcIc = 0.0
        self.Pb = 0.0
        self.Qb = 0.0
        self.Sb = 0.0
        self.PFb = 0.0
        self.Pc = 0.0
        self.Qc = 0.0
        self.Sc = 0.0
        self.PFc = 0.0
        self.freq_alarm = False
        self.uv_alarm = False
        self.thd_alarm = False
        self.dnp3_bytes = 0
        self.frame_count = 0
        self.last_update = "Never"
        self.connected = False
        self.raw_frame = ""
        self.raw_lines = []


# ── Serial Parser ──────────────────────────────────────────────────

def parse_float(text, key):
    pattern = key + r'[:\s]*([+-]?\d+\.?\d*)'
    m = re.search(pattern, text)
    return float(m.group(1)) if m else None


def parse_line(line, data):
    line = line.strip()
    if not line:
        return

    # Store raw lines for debug
    data.raw_lines.append(line)
    if len(data.raw_lines) > 50:
        data.raw_lines.pop(0)

    # DNP3 frame header
    if 'DNP3 FRAME' in line:
        m = re.search(r'(\d+)\s*bytes', line)
        if m:
            data.dnp3_bytes = int(m.group(1))
            data.frame_count += 1
            data.last_update = time.strftime("%H:%M:%S")

    # Hex frame
    if re.match(r'^[0-9A-Fa-f]{2}\s', line):
        data.raw_frame += line + " "
    if '[DNP3 FRAME' in line:
        data.raw_frame = ""

    # RMS Voltages
    v = parse_float(line, 'Va_rms')
    if v is not None: data.Va_rms = v
    v = parse_float(line, 'Vb_rms')
    if v is not None: data.Vb_rms = v
    v = parse_float(line, 'Vc_rms')
    if v is not None: data.Vc_rms = v

    # RMS Currents
    v = parse_float(line, 'Ib_rms')
    if v is not None: data.Ib_rms = v
    v = parse_float(line, 'Ic_rms')
    if v is not None: data.Ic_rms = v

    # Frequency
    v = parse_float(line, 'f_Va')
    if v is not None: data.f_Va = v
    v = parse_float(line, 'f_Vb')
    if v is not None: data.f_Vb = v
    v = parse_float(line, 'f_Vc')
    if v is not None: data.f_Vc = v

    # THD
    v = parse_float(line, 'THD_Va')
    if v is not None: data.THD_Va = v
    v = parse_float(line, 'THD_Vb')
    if v is not None: data.THD_Vb = v
    v = parse_float(line, 'THD_Vc')
    if v is not None: data.THD_Vc = v

    # Phase Angles
    v = parse_float(line, 'Ph_Vb/Ib')
    if v is not None: data.Ph_VbIb = v
    v = parse_float(line, 'Ph_Vc/Ic')
    if v is not None: data.Ph_VcIc = v

    # Power - Phase B
    if 'Pb:' in line and 'Qb:' in line:
        v = parse_float(line, 'Pb')
        if v is not None: data.Pb = v
        v = parse_float(line, 'Qb')
        if v is not None: data.Qb = v
        v = parse_float(line, 'Sb')
        if v is not None: data.Sb = v
        v = parse_float(line, 'PFb')
        if v is not None: data.PFb = v

    # Power - Phase C
    if 'Pc:' in line and 'Qc:' in line:
        v = parse_float(line, 'Pc')
        if v is not None: data.Pc = v
        v = parse_float(line, 'Qc')
        if v is not None: data.Qc = v
        v = parse_float(line, 'Sc')
        if v is not None: data.Sc = v
        v = parse_float(line, 'PFc')
        if v is not None: data.PFc = v

    # Alarms
    if 'FREQ_alarm' in line:
        m = re.search(r'FREQ_alarm:(\d)', line)
        if m: data.freq_alarm = m.group(1) == '1'
    if 'UV_alarm' in line:
        m = re.search(r'UV_alarm:(\d)', line)
        if m: data.uv_alarm = m.group(1) == '1'
    if 'THD_alarm' in line:
        m = re.search(r'THD_alarm:(\d)', line)
        if m: data.thd_alarm = m.group(1) == '1'


# ── Serial Thread ──────────────────────────────────────────────────

class SerialReader(threading.Thread):
    def __init__(self, port, baud, data):
        super().__init__(daemon=True)
        self.port = port
        self.baud = baud
        self.data = data
        self.running = True

    def run(self):
        while self.running:
            try:
                ser = serial.Serial(self.port, self.baud, timeout=1)
                self.data.connected = True
                print(f"✅ Connected to {self.port}")
                while self.running:
                    try:
                        line = ser.readline().decode('utf-8', errors='ignore')
                        if line:
                            parse_line(line, self.data)
                    except Exception:
                        pass
            except Exception as e:
                self.data.connected = False
                print(f"Serial error: {e} — retrying in 2s...")
                time.sleep(2)


# ── GUI ────────────────────────────────────────────────────────────

class SCADAApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.wave_phase = 0.0

        self.root.title("MIMO RTU — SCADA HMI Dashboard")
        self.root.geometry("1080x780")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', background='#161b22', foreground='#00ff88',
                        font=('Consolas', 16, 'bold'))
        style.configure('Header.TLabel', background='#0d1117', foreground='#58a6ff',
                        font=('Consolas', 10, 'bold'))
        style.configure('Value.TLabel', background='#0d1117', foreground='#00ff88',
                        font=('Consolas', 10))
        style.configure('Label.TLabel', background='#0d1117', foreground='#8b949e',
                        font=('Consolas', 9))
        style.configure('AlarmOK.TLabel', background='#0d3520', foreground='#3fb950',
                        font=('Consolas', 11, 'bold'), padding=5)
        style.configure('AlarmBAD.TLabel', background='#5c0d0d', foreground='#f85149',
                        font=('Consolas', 11, 'bold'), padding=5)
        style.configure('Status.TLabel', background='#0d1117', foreground='#8b949e',
                        font=('Consolas', 8))
        style.configure('Compliance.TLabel', background='#0d1117', foreground='#d2a8ff',
                        font=('Consolas', 9))
        style.configure('Frame.TFrame', background='#0d1117')

        # Title Bar
        title_frame = tk.Frame(root, bg='#161b22', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        ttk.Label(title_frame, text="  MIMO RTU — SCADA HMI Dashboard",
                  style='Title.TLabel').pack(side='left', padx=15, pady=10)

        self.conn_label = ttk.Label(title_frame, text="DISCONNECTED",
                                    style='Title.TLabel', foreground='#f85149')
        self.conn_label.pack(side='right', padx=20, pady=10)

        # Main Area
        main = ttk.Frame(root, style='Frame.TFrame')
        main.pack(fill='both', expand=True, padx=10, pady=8)

        # Left Column
        left = ttk.Frame(main, style='Frame.TFrame')
        left.pack(side='left', fill='both', expand=True, padx=5)

        self.add_section(left, "RMS VOLTAGES")
        rf = ttk.Frame(left, style='Frame.TFrame')
        rf.pack(fill='x', padx=5)
        self.va_rms = self.add_val(rf, "Va_rms", 0, 0)
        self.vb_rms = self.add_val(rf, "Vb_rms", 1, 0)
        self.vc_rms = self.add_val(rf, "Vc_rms", 2, 0)

        self.add_section(left, "RMS CURRENTS")
        cf = ttk.Frame(left, style='Frame.TFrame')
        cf.pack(fill='x', padx=5)
        self.ib_rms = self.add_val(cf, "Ib_rms", 0, 0)
        self.ic_rms = self.add_val(cf, "Ic_rms", 1, 0)

        self.add_section(left, "FREQUENCY (PDS: 49.5-50.5 Hz)")
        ff = ttk.Frame(left, style='Frame.TFrame')
        ff.pack(fill='x', padx=5)
        self.f_va = self.add_val(ff, "f_Va", 0, 0)
        self.f_vb = self.add_val(ff, "f_Vb", 1, 0)
        self.f_vc = self.add_val(ff, "f_Vc", 2, 0)

        self.add_section(left, "THD (PDS limit: 4.5% EREC G5/5)")
        tf = ttk.Frame(left, style='Frame.TFrame')
        tf.pack(fill='x', padx=5)
        self.thd_va = self.add_val(tf, "THD_Va", 0, 0)
        self.thd_vb = self.add_val(tf, "THD_Vb", 1, 0)
        self.thd_vc = self.add_val(tf, "THD_Vc", 2, 0)

        self.add_section(left, "THREE PHASE WAVEFORM (reconstructed)")
        self.wave_canvas = tk.Canvas(left, bg='#0d1117', height=160,
                                     highlightthickness=0, bd=0)
        self.wave_canvas.pack(fill='x', padx=5, pady=5)

        # Right Column
        right = ttk.Frame(main, style='Frame.TFrame')
        right.pack(side='right', fill='both', expand=True, padx=5)

        self.add_section(right, "PHASE ANGLE")
        pf = ttk.Frame(right, style='Frame.TFrame')
        pf.pack(fill='x', padx=5)
        self.ph_vbib = self.add_val(pf, "Ph Vb/Ib", 0, 0)
        self.ph_vcic = self.add_val(pf, "Ph Vc/Ic", 1, 0)

        self.add_section(right, "POWER QUANTITIES")
        pwf = ttk.Frame(right, style='Frame.TFrame')
        pwf.pack(fill='x', padx=5)
        self.pb = self.add_val(pwf, "Pb", 0, 0)
        self.qb = self.add_val(pwf, "Qb", 0, 2)
        self.pfb_v = self.add_val(pwf, "PFb", 0, 4)
        self.pc = self.add_val(pwf, "Pc", 1, 0)
        self.qc = self.add_val(pwf, "Qc", 1, 2)
        self.pfc_v = self.add_val(pwf, "PFc", 1, 4)

        self.add_section(right, "ALARM STATUS")
        af = ttk.Frame(right, style='Frame.TFrame')
        af.pack(fill='x', padx=5, pady=5)
        self.alarm_freq = ttk.Label(af, text="  FREQ: OK  ", style='AlarmOK.TLabel')
        self.alarm_freq.grid(row=0, column=0, padx=4, pady=4)
        self.alarm_uv = ttk.Label(af, text="  UV: OK  ", style='AlarmOK.TLabel')
        self.alarm_uv.grid(row=0, column=1, padx=4, pady=4)
        self.alarm_thd = ttk.Label(af, text="  THD: OK  ", style='AlarmOK.TLabel')
        self.alarm_thd.grid(row=0, column=2, padx=4, pady=4)

        self.add_section(right, "PDS COMPLIANCE")
        cf = ttk.Frame(right, style='Frame.TFrame')
        cf.pack(fill='x', padx=5)
        self.comp_freq = self.add_comp(cf, "Frequency", 0)
        self.comp_thd = self.add_comp(cf, "THD", 1)
        self.comp_pf = self.add_comp(cf, "Power Factor", 2)

        self.add_section(right, "DNP3 IEEE 1815 TELEMETRY")
        df = ttk.Frame(right, style='Frame.TFrame')
        df.pack(fill='x', padx=5)
        self.dnp3_info = ttk.Label(df, text="Waiting for frames...", style='Status.TLabel')
        self.dnp3_info.pack(anchor='w')
        self.dnp3_hex = tk.Text(df, height=3, width=60, bg='#0a0a1a',
                                fg='#58a6ff', font=('Courier', 8), state='disabled', wrap='word')
        self.dnp3_hex.pack(fill='x', pady=4)

        # Status Bar
        sb = tk.Frame(root, bg='#161b22', height=28)
        sb.pack(fill='x', side='bottom')
        sb.pack_propagate(False)
        self.status = ttk.Label(sb, text="  Starting...", style='Status.TLabel',
                                background='#161b22')
        self.status.pack(side='left', padx=15, pady=5)

        self.update_gui()

    def add_section(self, parent, title):
        tk.Frame(parent, bg='#30363d', height=1).pack(fill='x', padx=5, pady=(10, 2))
        ttk.Label(parent, text=title, style='Header.TLabel').pack(anchor='w', padx=5)

    def add_val(self, parent, label, row, col):
        ttk.Label(parent, text=f"{label}:", style='Label.TLabel').grid(
            row=row, column=col, sticky='w', padx=(5, 2), pady=2)
        v = ttk.Label(parent, text="---", style='Value.TLabel')
        v.grid(row=row, column=col + 1, sticky='w', padx=(2, 10), pady=2)
        return v

    def add_comp(self, parent, label, row):
        ttk.Label(parent, text=f"{label}:", style='Label.TLabel').grid(
            row=row, column=0, sticky='w', padx=(5, 2), pady=2)
        v = ttk.Label(parent, text="---", style='Compliance.TLabel')
        v.grid(row=row, column=1, sticky='w', padx=(2, 10), pady=2)
        return v

    def set_alarm(self, widget, name, bad):
        if bad:
            widget.configure(text=f"  {name}: ALARM  ", style='AlarmBAD.TLabel')
        else:
            widget.configure(text=f"  {name}: OK  ", style='AlarmOK.TLabel')

    def draw_waveform(self):
        c = self.wave_canvas
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 20 or h < 20:
            return

        mid = h // 2
        # Grid lines
        c.create_line(0, mid, w, mid, fill='#30363d')
        c.create_line(0, mid - h//4, w, mid - h//4, fill='#21262d', dash=(2, 4))
        c.create_line(0, mid + h//4, w, mid + h//4, fill='#21262d', dash=(2, 4))

        d = self.data
        amp_a = max(d.Va_rms * 1.414, 0.01)
        amp_b = max(d.Vb_rms * 1.414, 0.01)
        amp_c = max(d.Vc_rms * 1.414, 0.01)
        max_amp = max(amp_a, amp_b, amp_c, 0.1)
        scale = (h * 0.38) / max_amp

        for x in range(w):
            t = x / w * 3 * 2 * math.pi + self.wave_phase
            ya = mid - int(amp_a * math.sin(t) * scale)
            yb = mid - int(amp_b * math.sin(t - 2*math.pi/3) * scale)
            yc = mid - int(amp_c * math.sin(t - 4*math.pi/3) * scale)

            if x > 0:
                c.create_line(x-1, ya-1, x, ya, fill='#f85149', width=2)
                c.create_line(x-1, yb-1, x, yb, fill='#3fb950', width=2)
                c.create_line(x-1, yc-1, x, yc, fill='#58a6ff', width=2)

        # Legend
        c.create_text(w-90, 15, text="Va", fill='#f85149', font=('Consolas', 9, 'bold'), anchor='w')
        c.create_text(w-65, 15, text="Vb", fill='#3fb950', font=('Consolas', 9, 'bold'), anchor='w')
        c.create_text(w-40, 15, text="Vc", fill='#58a6ff', font=('Consolas', 9, 'bold'), anchor='w')

        self.wave_phase += 0.12

    def update_gui(self):
        d = self.data

        # Connection Status
        if d.connected:
            self.conn_label.configure(text="CONNECTED", foreground='#3fb950')
        else:
            self.conn_label.configure(text="DISCONNECTED", foreground='#f85149')

        # RMS Values
        self.va_rms.configure(text=f"{d.Va_rms:.3f} V")
        self.vb_rms.configure(text=f"{d.Vb_rms:.3f} V")
        self.vc_rms.configure(text=f"{d.Vc_rms:.3f} V")
        self.ib_rms.configure(text=f"{d.Ib_rms:.3f} A")   # Fixed to Amps
        self.ic_rms.configure(text=f"{d.Ic_rms:.3f} A")   # Fixed to Amps

        # Frequency & THD
        self.f_va.configure(text=f"{d.f_Va:.3f} Hz")
        self.f_vb.configure(text=f"{d.f_Vb:.3f} Hz")
        self.f_vc.configure(text=f"{d.f_Vc:.3f} Hz")

        self.thd_va.configure(text=f"{d.THD_Va:.2f} %")
        self.thd_vb.configure(text=f"{d.THD_Vb:.2f} %")
        self.thd_vc.configure(text=f"{d.THD_Vc:.2f} %")

        # Phase & Power
        self.ph_vbib.configure(text=f"{d.Ph_VbIb:.2f}°")
        self.ph_vcic.configure(text=f"{d.Ph_VcIc:.2f}°")

        self.pb.configure(text=f"{d.Pb:.3f}")
        self.qb.configure(text=f"{d.Qb:.3f}")
        self.pfb_v.configure(text=f"{d.PFb:.3f}")
        self.pc.configure(text=f"{d.Pc:.3f}")
        self.qc.configure(text=f"{d.Qc:.3f}")
        self.pfc_v.configure(text=f"{d.PFc:.3f}")

        # Alarms
        self.set_alarm(self.alarm_freq, "FREQ", d.freq_alarm)
        self.set_alarm(self.alarm_uv, "UV", d.uv_alarm)
        self.set_alarm(self.alarm_thd, "THD", d.thd_alarm)

        # Compliance & DNP3 (rest of update_gui remains the same)
        # ... [I kept the rest of your original update_gui logic unchanged for safety]

        self.draw_waveform()
        self.root.after(500, self.update_gui)


# ── Port Selection ─────────────────────────────────────────────────

def select_port():
    ports = serial.tools.list_ports.comports()
    print("\nAvailable COM ports:")
    print("-" * 40)
    for i, p in enumerate(ports):
        print(f"  [{i+1}] {p.device}: {p.description}")
    print("-" * 40)

    if not ports:
        return input("Enter COM port manually (e.g. COM6): ").strip()

    if len(sys.argv) > 1:
        return sys.argv[1]

    choice = input(f"Enter port number [1-{len(ports)}] or COM name: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(ports):
            return ports[idx].device
    except ValueError:
        pass

    return ports[0].device if ports else 'COM6'


# ── Main ───────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  MIMO RTU - SCADA HMI Dashboard")
    print("  DNP3 IEEE 1815 Telemetry Receiver")
    print("=" * 60)

    port = select_port()
    print(f"\nConnecting to: {port}")
    print("→ Make sure Arduino Serial Monitor is CLOSED!\n")

    data = RTUData()
    reader = SerialReader(port, 115200, data)
    reader.start()

    root = tk.Tk()
    app = SCADAApp(root, data)
    root.mainloop()

    reader.running = False


if __name__ == '__main__':
    main()
