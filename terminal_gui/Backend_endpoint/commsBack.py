import socket
import threading

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(2048).decode()
            if not message:
                break
            print(f"Client says: {message}")
            # Send a response back to the client
            response = input("Enter response to client: ")
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
