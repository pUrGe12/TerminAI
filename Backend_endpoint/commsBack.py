import socket
import threading

SEQUENCER_PORT = 65000

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(2048).decode()
            if not message:
                break
            print(f"Client says: {message}")
            
            # Only create and connect the sequencer socket when a message is received
            sequencer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sequencer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sequencer_socket.connect(('127.0.0.1', SEQUENCER_PORT))
                sequencer_socket.send(message.encode())  # Send the message to the sequencer
                sequencer_socket.close()  # Close the socket after sending
            except ConnectionRefusedError:
                print("Failed to connect to the sequencer. Ensure it is running.")

            response = input("Enter response to client: ")  # Modify this to send the response by Model S later
            client_socket.send(response.encode())
        except ConnectionResetError:
            print("Client disconnected.")
            break

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", 64920))  # Use any available port
    server_socket.listen(5)
    print("Server is listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
