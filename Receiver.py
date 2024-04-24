import bluetooth

def setup_server():
    """Set up Bluetooth server socket."""
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1  # Commonly used port for Bluetooth communication
    server_sock.bind(("", port))
    server_sock.listen(1)
    print("Listening for a connection on RFCOMM channel %d" % port)
    return server_sock

def accept_connection(server_sock):
    """Accept a connection from a client."""
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")
    return client_sock

def process_commands(client_sock):
    """Process incoming commands from the connected Bluetooth device."""
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            # Here you could add command processing logic
            respond_to_command(data.decode('utf-8'), client_sock)
    except bluetooth.btcommon.BluetoothError as err:
        print(f"Bluetooth Error: {err}")
    finally:
        client_sock.close()

def respond_to_command(command, client_sock):
    """Send a response back to the client based on the command."""
    response = f"Processed command: {command}"
    client_sock.send(response.encode('utf-8'))
    print(f"Sent response: {response}")

def main():
    server_sock = setup_server()
    try:
        while True:
            client_sock = accept_connection(server_sock)
            process_commands(client_sock)
    finally:
        server_sock.close()
        print("Server socket closed.")

if __name__ == "__main__":
    main()
