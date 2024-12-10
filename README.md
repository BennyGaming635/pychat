### PyChat: Local Network CLI Chatroom

PyChat is a Python-based CLI chatroom that runs on a local network. It allows users to connect, chat, and interact using commands.

---

### Features:
- **Local Network Communication**: Automatically discovers and connects to the PyChat server.
- **Channels**: Create and join chat channels.
- **Admin Commands**:
  - `/kick <username>`: Kick a user for 1 minute.
  - `/ban <username> <days>`: Ban a user for a specified number of days.
  - `/cc <channel-name>`: Create a new channel.
- **User Commands**:
  - `/channels`: List all available channels.
  - `/joinc <channel-name>`: Join a specific channel.
  - `/help`: Display a list of available commands.
- **Achievements and Badges**: Earn rewards for actions like sending your first message.

---

### Getting Started:
1. **Run the Server**:
   ```bash
   python pychat_server.py
   ```
2. **Connect Clients**:
   ```bash
   python pychat_client.py
   ```

---

### Requirements:
- Python 3.x
- Works on a local network (ensure all devices are on the same network).

---

### Notes:
- For the best experience, ensure the server is running before clients attempt to connect.
- Customize the server and client IP/PORT settings if needed.