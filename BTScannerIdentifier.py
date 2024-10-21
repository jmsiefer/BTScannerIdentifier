import tkinter as tk
from tkinter import messagebox
import asyncio
import threading

from bleak import BleakScanner, BleakClient
import traceback

class BluetoothScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluetooth Scanner")
        self.devices = []
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.run_event_loop, daemon=True).start()
        self.scanning_event = None  # Will be initialized during scanning
        self.scanning_task = None   # Reference to the scanning task
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.scan_button = tk.Button(button_frame, text="Scan BT Devices", command=self.scan_for_devices)
        self.scan_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Create a listbox to display devices
        self.device_listbox = tk.Listbox(self.root, width=80)
        self.device_listbox.pack(padx=10, pady=10)

        # Create a label for status updates
        self.status_label = tk.Label(self.root, text="Ready")
        self.status_label.pack(pady=5)

    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def scan_for_devices(self):
        self.scan_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.device_listbox.delete(0, tk.END)
        self.devices.clear()
        self.update_status("Starting scan...")
        # Start scanning for devices
        self.root.after(100, self.start_scanning)

    def stop_scanning(self):
        if self.scanning_event:
            self.scanning_event.set()
            self.update_status("Stopping scan...")

    def start_scanning(self):
        # Initialize the scanning event
        self.scanning_event = asyncio.Event()
        # Start scanning for devices and check connection security
        self.scanning_task = asyncio.run_coroutine_threadsafe(self.scan_and_check_devices(), self.loop)
        self.scanning_task.add_done_callback(lambda f: self.process_scan_results(f.result()))

    async def scan_and_check_devices(self):
        devices = []
        self.update_status("Scanning for BLE devices...")
        try:
            ble_devices = await BleakScanner.discover()
            total_devices = len(ble_devices)
            if total_devices == 0:
                self.update_status("No BLE devices found.")
                return devices
            self.update_status(f"Found {total_devices} devices. Checking each device...")
            device_counter = 0
            for d in ble_devices:
                if self.scanning_event.is_set():
                    self.update_status("Scan stopped by user.")
                    break
                device_counter += 1
                self.update_status(f"Checking device {device_counter}/{total_devices}: {d.name or 'Unknown'}")
                device_info = {'name': d.name or 'Unknown', 'address': d.address}
                # Attempt to connect to the device to check if it requires security
                try:
                    client = BleakClient(d.address)
                    await client.connect(timeout=5.0)
                    # If connection is successful, services should be automatically discovered
                    services = client.services
                    if services and len(services) > 0:
                        device_info['connectable_without_security'] = True
                    else:
                        device_info['connectable_without_security'] = False
                    await client.disconnect()
                except Exception as e:
                    # If connection fails, the device may require security or be non-connectable
                    device_info['connectable_without_security'] = False
                    # Optionally log the exception
                    # print(f"Failed to connect to {d.name} ({d.address}): {e}")
                devices.append(device_info)
            self.devices = devices  # Store the devices found so far
        except Exception as e:
            self.update_status(f"Error scanning for BLE devices: {e}")
            traceback.print_exc()
        return devices

    def process_scan_results(self, devices):
        # Display the devices
        for device in devices:
            name = device['name']
            connectable = device.get('connectable_without_security', False)
            if connectable:
                connect_status = "Connectable without security"
            else:
                connect_status = "Requires security or cannot connect"
            display_text = f"Name: {name}, Address: {device['address']}, {connect_status}"
            self.device_listbox.insert(tk.END, display_text)

        self.scan_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if devices:
            if self.scanning_event.is_set():
                self.update_status("Scan stopped. Partial results displayed.")
            else:
                self.update_status("Scan complete.")
        else:
            self.update_status("No devices found.")
        self.root.title("Bluetooth BLE Scanner")
        self.scanning_event = None  # Reset the scanning event
        self.scanning_task = None   # Clear the scanning task

    def update_status(self, message):
        self.status_label.config(text=message)
        self.status_label.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothScannerApp(root)
    root.mainloop()
