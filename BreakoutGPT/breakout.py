import socket
import json

class Listener65032:
    def __init__(self, port=65032):
        self.port = port
        self.running = True
        # UDP socket for receiving messages
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(('127.0.0.1', self.port))

    def listen(self):
        print(f"Listening for messages on port {self.port}...")
        while self.running:
            try:
                data, addr = self.receive_socket.recvfrom(1024)
                received_data = json.loads(data.decode('utf-8'))
                print(f"\nReceived message from {addr}: {received_data['message']}")
                print(f"Timestamp: {received_data['timestamp']}")
                print(f"Sender: {received_data['sender']}")
                print(f"Sysbool: {received_data['sysbool']}")
                print(f"prompt: {received_data['prompt']}")
            except json.JSONDecodeError:
                print(f"\nReceived malformed data from {addr}")
            except Exception as e:
                if self.running:
                    print(f"\nError while listening: {e}")

    def close(self):
        self.running = False
        self.receive_socket.close()

if __name__ == "__main__":
    listener = Listener65032()
    try:
        listener.listen()
    except KeyboardInterrupt:
        print("\nShutting down listener...")
    finally:
        listener.close()
