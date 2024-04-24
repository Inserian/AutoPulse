import bluetooth
import sys

def find_device(device_name):
    """Scan for the given device by name and return its address."""
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    target_address = None
    for addr, name in devices:
        if device_name == name:
            target_address = addr
            break
    return target_address

def connect_device(device_address):
    """Create a Bluetooth connection to the device and return the socket."""
    port = 1  # Bluetooth port number, often it's 1, but depends on the device
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
        sock.connect((device_address, port))
        print("Connected to the device successfully.")
    except bluetooth.btcommon.BluetoothError as err:
        print("Could not connect to the device: ", err)
        sock.close()
        sys.exit()
    return sock

def send_command(sock, command):
    """Send a command to the device."""
    try:
        sock.send(command)
        print(f"Sent command: {command}")
    except bluetooth.btcommon.BluetoothError as err:
        print("Failed to send command: ", err)

def main():
    device_name = "IVControlDevice"  # Change this to your device's Bluetooth name
    device_address = find_device(device_name)

    if device_address is None:
        print("Could not find the device. Please make sure it is turned on and discoverable.")
        return

    sock = connect_device(device_address)
    
    # Example commands
    send_command(sock, "SET DOSE 5ml")
    send_command(sock, "START INJECTION")

    sock.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
