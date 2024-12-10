import socket
import threading
import time

DISCOVERY_PORT = 12344
CHAT_PORT = 12345

# Attempt to discover the server on the local network
def discover_server():
    """Broadcast a discovery message to find the PyChat server."""
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    discovery_socket.settimeout(5)  # Timeout after 5 seconds

    try:
        discovery_message = "PYCHAT_DISCOVERY".encode()
        discovery_socket.sendto(discovery_message, ('255.255.255.255', DISCOVERY_PORT))
        print("Searching for PyChat server...")

        # Wait for a response from the server
        while True:
            try:
                response, server_address = discovery_socket.recvfrom(1024)
                if response.decode() == "PYCHAT_SERVER":
                    print(f"Found server at {server_address[0]}")
                    return server_address[0]
            except socket.timeout:
                break
    except Exception as e:
        print(f"Discovery error: {e}")
    finally:
        discovery_socket.close()

    return None

# Listen for incoming messages
def receive_messages(client_socket):
    """Receive and display messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
            else:
                break
        except:
            print("Connection to the server has been lost.")
            break

# Main client function
def start_client():
    """Start the PyChat client and connect to the server."""
    server_ip = discover_server()
    if not server_ip:
        print("Server discovery timed out.\nCould not find a PyChat server.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, CHAT_PORT))
        print("Connected to the PyChat server!")

        # Start a thread to listen for incoming messages
        threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

        # Send messages to the server
        while True:
            message = input("> ")
            if message.lower() == "/quit":
                print("Exiting PyChat...")
                client_socket.close()
                break
            else:
                client_socket.send(message.encode())

    except Exception as e:
        print(f"Error connecting to the server: {e}")

if __name__ == "__main__":
    start_client()
