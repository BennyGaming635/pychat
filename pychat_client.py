import socket
import threading
import time

HOST = '127.0.0.1'  # Localhost for testing
CHAT_PORT = 12345
DISCOVERY_PORT = 12344

clients = {}  # Store client socket and username
banned_users = {}  # Store banned users and their ban expiry times
channels = {}  # Store channels and their members

# Kick timer
kick_timers = {}

def handle_client(client, addr):
    """Handles an individual client."""
    # Ask for a username
    client.send("Enter a username: ".encode())
    username = client.recv(1024).decode()
    clients[client] = username
    print(f"{username} has joined the server from {addr}")
    
    # Send welcome message
    client.send(f"Welcome {username}! Type /help for commands.\n".encode())
    
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                process_message(message, client, username)
            else:
                break
        except:
            break

    remove_client(client, username)

def process_message(message, client, username):
    """Processes incoming messages and handles commands."""
    if message.startswith("/"):
        # Command handling
        command_parts = message.split()
        command = command_parts[0].lower()
        
        if command == "/kick" and len(command_parts) == 2:
            kick_user(command_parts[1], username)
        elif command == "/ban" and len(command_parts) == 3:
            ban_user(command_parts[1], int(command_parts[2]), username)
        elif command == "/cc" and len(command_parts) == 2:
            create_channel(command_parts[1], client)
        elif command == "/channels":
            list_channels(client)
        elif command == "/joinc" and len(command_parts) == 2:
            join_channel(command_parts[1], client)
        elif command == "/help":
            show_help(client)
        else:
            client.send("Invalid command. Type /help for a list of commands.\n".encode())
    else:
        # Regular message handling (broadcast)
        broadcast(message, client, username)

def broadcast(message, sender_client, sender_username):
    """Broadcast a message to all clients."""
    for client, username in clients.items():
        if client != sender_client:
            client.send(f"{sender_username}: {message}\n".encode())

def kick_user(username, admin_username):
    """Kick a user for 1 minute."""
    for client, user in clients.items():
        if user == username:
            kick_timers[client] = time.time() + 60  # 60 seconds ban
            client.send(f"You have been kicked for 1 minute by {admin_username}\n".encode())
            break

def ban_user(username, days, admin_username):
    """Ban a user for a specified number of days."""
    for client, user in clients.items():
        if user == username:
            banned_users[user] = time.time() + (days * 86400)  # Ban duration in seconds
            client.send(f"You have been banned for {days} days by {admin_username}\n".encode())
            break

def create_channel(channel_name, client):
    """Create a new channel."""
    if channel_name not in channels:
        channels[channel_name] = [client]  # Add the creator to the channel
        client.send(f"Channel '{channel_name}' created and you joined it.\n".encode())
    else:
        client.send(f"Channel '{channel_name}' already exists.\n".encode())

def list_channels(client):
    """List all channels."""
    if channels:
        channel_list = "\n".join([channel for channel in channels])
        client.send(f"Channels available:\n{channel_list}\n".encode())
    else:
        client.send("No channels available.\n".encode())

def join_channel(channel_name, client):
    """Join an existing channel."""
    if channel_name in channels:
        channels[channel_name].append(client)
        client.send(f"You have joined the channel '{channel_name}'.\n".encode())
    else:
        client.send(f"Channel '{channel_name}' does not exist.\n".encode())

def remove_client(client, username):
    """Removes a client from the server."""
    if client in clients:
        del clients[client]
        print(f"{username} has left the server.")
        broadcast(f"{username} has left the chat.\n", client, username)

def show_help(client):
    """Display the help message with available commands."""
    help_message = """
    Available Commands:
    /kick <username> - Kick a user for 1 minute.
    /ban <username> <days> - Ban a user for a specified number of days.
    /cc <channel-name> - Create a new channel.
    /channels - List all available channels.
    /joinc <channel-name> - Join a channel.
    /help - Show this help message.
    """
    client.send(help_message.encode())

def handle_kicks_and_bans():
    """Check for kicked or banned users."""
    while True:
        for client in list(kick_timers.keys()):
            if time.time() > kick_timers[client]:
                client.send("You are no longer kicked and can join the chat.\n".encode())
                del kick_timers[client]
        
        for user in list(banned_users.keys()):
            if time.time() > banned_users[user]:
                del banned_users[user]

        time.sleep(10)

def start_chat_server():
    """Starts the main chat server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, CHAT_PORT))
    server.listen()
    print(f"Chat server listening on {HOST}:{CHAT_PORT}")

    # Start the kick and ban handler thread
    threading.Thread(target=handle_kicks_and_bans, daemon=True).start()

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    start_chat_server()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
