import tkinter as tk
from tkinter import ttk
import socket
import threading


def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)  # Set timeout to half a second
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
    except:
        return False
    finally:
        sock.close()


class PortScannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x250")
        self.root.title("Port Scanner")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10)

        self.port_scan_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.port_scan_tab, text="Port Scan")

        self.ip_frame = tk.Frame(self.port_scan_tab)
        self.ip_frame.pack()

        self.ip_label = tk.Label(self.ip_frame, text="Enter IP address:")
        self.ip_label.pack(side=tk.LEFT)

        self.ip_entry = tk.Entry(self.ip_frame)
        self.ip_entry.pack(side=tk.LEFT)

        self.port_frame = tk.Frame(self.port_scan_tab)
        self.port_frame.pack()

        self.port_label = tk.Label(self.port_frame, text="Enter port range:")
        self.port_label.pack(side=tk.LEFT)

        self.port_entry1 = tk.Entry(self.port_frame, width=5)
        self.port_entry1.pack(side=tk.LEFT)

        self.port_label2 = tk.Label(self.port_frame, text="-")
        self.port_label2.pack(side=tk.LEFT)

        self.port_entry2 = tk.Entry(self.port_frame, width=5)
        self.port_entry2.pack(side=tk.LEFT)

        self.scan_button = tk.Button(self.port_scan_tab, text="Scan Ports", command=self.start_scan)
        self.scan_button.pack(pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.port_scan_tab, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)

        self.result_text = tk.Text(self.port_scan_tab, height=8, width=40)
        self.result_text.pack()

    def start_scan(self):
        ip = self.ip_entry.get()
        port1 = int(self.port_entry1.get())
        port2 = int(self.port_entry2.get())

        self.progress_var.set(0)

        def scan_ports():
            results = []
            for port in range(port1, port2+1):
                if is_port_open(ip, port):
                    results.append(f"Port {port} is working")
                else:
                    results.append(f"Port {port} is not working")
                self.progress_var.set((port - port1 + 1) / (port2 - port1 + 1) * 100)
            self.show_results("\n".join(results))

        t = threading.Thread(target=scan_ports)
        t.start()

    def show_results(self, results):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, results)


if __name__ == "__main__":
    app = PortScannerApp()
    app.root.mainloop()
