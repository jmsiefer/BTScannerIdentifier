
# Bluetooth Scanner GUI

A Python application with a Tkinter GUI that scans for Bluetooth Low Energy (BLE) devices, attempts to connect to them to check if they require security, and allows the user to stop the scan and receive partial results.

## Features

- **Scan for BLE Devices**: Discover nearby BLE devices and attempt to connect to them.
- **Check Connection Security**: Determine if devices can be connected to without security measures.
- **Stop Scan Anytime**: Provides a **"Stop"** button to halt the scanning process and display partial results.
- **User-Friendly GUI**: Built with Tkinter for a simple and intuitive interface.
- **Real-Time Status Updates**: Displays scanning progress and status messages.

## Prerequisites

- **Python 3.6 or higher**
- **Bleak Library**: For BLE scanning and connections.
- **Tkinter**: For the graphical user interface.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/bluetooth-ble-scanner-gui.git
   cd bluetooth-ble-scanner-gui
   ```

2. **Create a Virtual Environment (Optional)**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or macOS
   source venv/bin/activate
   ```

3. **Install Required Libraries**

   ```bash
   pip install bleak
   ```

   - **Note**: Tkinter is usually included with Python installations on Windows and macOS. On Linux, you may need to install it separately:

     - For Debian/Ubuntu:

       ```bash
       sudo apt-get install python3-tk
       ```

     - For Fedora:

       ```bash
       sudo dnf install python3-tkinter
       ```

## Usage

1. **Run the Application**

   Save the provided script as `ble_scanner_gui.py`, then run:

   ```bash
   python ble_scanner_gui.py
   ```

2. **Using the GUI**

   - **Scan BLE Devices**: Click the **"Scan BLE Devices"** button to start scanning.
   - **Stop Scanning**: Click the **"Stop"** button to halt the scan and display partial results.
   - **View Results**: Devices found are listed with their name, address, and connection status.

3. **Understanding the Output**

   - **Name**: The device's name (or "Unknown" if not available).
   - **Address**: The MAC address of the device.
   - **Connection Status**:
     - **Connectable without security**: Device can be connected to without pairing or authentication.
     - **Requires security or cannot connect**: Device requires security measures or cannot be connected to.

## Notes

- **Permissions**:
  - On **Windows**, you may need to run the application with administrator privileges.
  - On **Linux**, you might need to run the script with `sudo` or adjust Bluetooth permissions.
- **Limitations**:
  - Scanning may take time depending on the number of devices in the vicinity.
  - Connection attempts may be rejected by devices requiring pairing or security.
- **Privacy Considerations**:
  - Be mindful of privacy and legal guidelines when scanning for and attempting to connect to devices.
  - Modify the script to perform passive scanning if you prefer not to initiate connections.

## Troubleshooting

- **No Devices Found**:
  - Ensure your Bluetooth adapter is enabled and functioning.
  - Make sure the devices are powered on and within range.
- **Permission Errors**:
  - Check that you have the necessary permissions to access Bluetooth devices.
  - On Linux, you may need to add your user to the `bluetooth` group.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the [Bleak](https://github.com/hbldh/bleak) library for providing a cross-platform BLE interface.
- Inspired by the need for a simple BLE scanning tool with a GUI.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with improvements or bug fixes.

---

**Disclaimer**: This application is for educational and testing purposes. Always ensure you have permission before scanning for and connecting to devices.
