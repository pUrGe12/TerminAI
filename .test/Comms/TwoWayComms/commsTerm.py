import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(2048).decode()
            if not message:
                break
            print(f"Server says: {message}")
        except ConnectionResetError:
            print("Server disconnected.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 64920))  # Replace with server IP if needed
    print("Connected to the server.")

    # Start a thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter message to server: ")
        client_socket.send(message.encode())

if __name__ == "__main__":
    start_client()
