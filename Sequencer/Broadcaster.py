import socket
import threading
import time
import json
import queue
from supabase import create_client, Client                                  # For database adding and pulling
from address import function_dict, address_dict                             # For getting information on the models, to add to database

#                                                                        Initialising the database

url: str = "https://yvcmpdgbeopnscegtjoh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y21wZGdiZW9wbnNjZWd0am9oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAzNjAxMzUsImV4cCI6MjA0NTkzNjEzNX0.n2FKKYLLO_IhtWtjsZfNSVic5mnuXmu5dCA9mbk1SfU"

supabase: Client = create_client(url, key)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                        Broadcasting and listening
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

class BroadcasterListener:
    '''
    This class creates a broadcast instance that asynchronously sends data to multiple models,
    while a daemon listens for incoming connections on a different thread.
    
    This uses a queue to push the received data into it. 
    '''

    def __init__(self, broadcast_ports, listen_port):
        self.broadcast_ports = broadcast_ports
        self.listen_port = listen_port
        self.running = True
        self.message_queue = queue.Queue()  # Queue to store received messages for external access
        
        # UDP socket for broadcasting
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # UDP socket for listening
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(('', self.listen_port))
        
        # Listener thread
        self.listener_thread = threading.Thread(target=self.listen_for_messages)
        self.listener_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        self.listener_thread.start()
    
    def broadcast_message(self, message, history):
        """
        Broadcasts a message and a history list to all models.
        """
        
        assert isinstance(history, list), 'history is wrongly formatted'
        data = {
            'message': message,
            'history': history,
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
        """
        Pretty-printing of the received message and adding it to the queue for external access.
        """
        print(f"\nReceived from {addr}: {received_data['message']}")
        print(f"Timestamp: {received_data['timestamp']}")
        print(f"Sender: {received_data['sender']}")
        print(f"sysbool: {received_data['sysbool']}")
        print("\nEnter message to broadcast (or 'quit' to exit): ", end='', flush=True)
        
        # Add the received data to the queue
        self.message_queue.put(received_data)

    def listen_for_messages(self):
        """
        Listens for incoming messages on the specified port.
        """
        print(f"Listening for messages on port {self.listen_port}...")
        while self.running:
            try:
                data, addr = self.listen_socket.recvfrom(1024)
                received_data = json.loads(data.decode('utf-8'))
                # Use a separate thread to handle the received message
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

    def get_received_messages(self):
        """Retrieve all messages currently in the queue."""
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages
    
    def close(self):
        """Clean up and close all connections."""
        self.running = False
        self.broadcast_socket.close()
        self.listen_socket.close()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#               
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_prompt():
    """
    This function is being used to get input from the breakout code. We've created a socket connection between these two and it simply recieves data.
    
    (for the time being, we've just using input)
    """
    try:
        return input("Enter message to broadcast (or 'quit' to exit): ")
    except EOFError:
        return 'quit'

def get_history():
    """
    This function queries supabase and gets the last five data points, and returns a list of the required parameters
    """

    response = supabase.table('History').select("*").order('id', desc=True).limit(5).execute().data
    return response
    
def add_history(name, system_boolean, prompt):
    """
    This function is to be called whenever the broadcaster receives data from any node. When it recieves data, it means the node must've fired up. 
    It will extract the relevant data from the node and add that to the database for further history implementation.

    This is to be called after querying the database, so that the current input is not regarded as history.
    """
    Info = {'M_addr': f"{address_dict.get(name)}", 'SysBool': f"{system_boolean}", 'M_func': f"{function_dict.get(name)}", 'Prompt': f"{prompt}"}
    response = supabase.table('History').insert(Info).execute()
    

if __name__ == "__main__":

    BROADCAST_PORTS = [5000+i for i in range(1,4)]  # Ports to broadcast to
    LISTEN_PORT = 5000  # Port to listen on
    broadcaster = BroadcasterListener(BROADCAST_PORTS, LISTEN_PORT)

    try:
        while True:
            history = get_history()
            prompt = get_prompt()
            if prompt.lower() == 'quit':
                break
            broadcaster.broadcast_message(prompt, history)
            if not broadcaster.message_queue.empty():
                messages = broadcaster.message_queue.get()
                system_boolean = messages['sysbool']
                name = f"client_{messages['sender'].split('-')[1]}"
                add_history(name, system_boolean, prompt)
                print('added history')  

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        broadcaster.close()