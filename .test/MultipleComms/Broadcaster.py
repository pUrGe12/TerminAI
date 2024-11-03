import socket
import threading
import time
import json

class BroadcasterListener:
    def __init__(self, broadcast_ports, listen_port):
        self.broadcast_ports = broadcast_ports
        self.listen_port = listen_port
        self.running = True
        
        # Create UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Create UDP socket for listening
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', self.listen_port))
        
        # Start listener thread
        self.listener_thread = threading.Thread(target=self.listen_for_messages)
        self.listener_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        self.listener_thread.start()
    
    def broadcast_message(self, message):
        """Broadcast a message to all specified ports"""
        data = {
            'message': message,
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': f'Broadcaster-{self.listen_port}'
        }
        encoded_data = json.dumps(data).encode('utf-8')
        
        try:
            for port in self.broadcast_ports:
                self.broadcast_socket.sendto(encoded_data, ('255.255.255.255', port))
                print(f"\nBroadcasted to port {port}: {message}")
        except Exception as e:
            print(f"\nError broadcasting message: {e}")

    def print_received_message(self, addr, received_data):
        """Print received message without interrupting input"""
        print(f"\nReceived from {addr}: {received_data['message']}")
        print(f"Timestamp: {received_data['timestamp']}")
        print(f"Sender: {received_data['sender']}")
        print("\nEnter message to broadcast (or 'quit' to exit): ", end='', flush=True)
    
    def listen_for_messages(self):
        """Listen for incoming messages"""
        print(f"Listening for messages on port {self.listen_port}...")
        while self.running:
            try:
                data, addr = self.listen_socket.recvfrom(1024)
                received_data = json.loads(data.decode('utf-8'))
                # Use a separate thread to print the received message
                print_thread = threading.Thread(
                    target=self.print_received_message,
                    args=(addr, received_data)
                )
                print_thread.start()
            except json.JSONDecodeError:
                print(f"\nReceived malformed data from {addr}")
            except Exception as e:
                if self.running:  # Only print error if we're still running
                    print(f"\nError while listening: {e}")
    
    def close(self):
        """Clean up resources"""
        self.running = False
        self.broadcast_socket.close()
        self.listen_socket.close()

def get_input():
    """Get input from user without being interrupted by received messages"""
    try:
        return input("Enter message to broadcast (or 'quit' to exit): ")
    except EOFError:
        return 'quit'

if __name__ == "__main__":
    # Example usage as broadcaster
    BROADCAST_PORTS = [5001, 5002, 5003]  # Ports to broadcast to
    LISTEN_PORT = 5000  # Port to listen on
    
    broadcaster = BroadcasterListener(BROADCAST_PORTS, LISTEN_PORT)
    
    try:
        while True:
            message = get_input()
            if message.lower() == 'quit':
                break
            broadcaster.broadcast_message(message)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        broadcaster.close()