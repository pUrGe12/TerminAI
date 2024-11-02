import socket
import threading
import time
import json
import queue
from supabase import create_client, Client                                     # For database adding and pulling
from address import function_dict                                              # For getting information on the models, to add to database
from api_keys import supabase_key_dict

url: str = str(supabase_key_dict.get('url'))
key: str = str(supabase_key_dict.get('key'))

supabase: Client = create_client(url, key)

TIMES_RAN = 1

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
        self.message_queue = queue.Queue()      # Queue to store data from the models
        self.prompt_queue = queue.Queue()       # Queue to store data from the backend endpoint
        

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
        self.listener_thread.daemon = True                          # Make thread daemon so it exits when main thread exits
        self.listener_thread.start()
    
    def broadcast_message(self, message, history):
        """
        Broadcasts a message and a history list to all models. The history directly pulled contains weird stuff that is not really of any sense to the models. 
        
        Make sure the history passed here contains only the relevant things.
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

                # Separate thread to handle the received message

                print_thread = threading.Thread(
                target=self.print_received_message,
                args=(addr, received_data)
                )
                print_thread.start()
            except json.JSONDecodeError:
                print(f"\nReceived malformed data from {addr}")
            except Exception as e:
                if self.running:                                        # only print error if we're still running
                    print(f"\nError while listening: {e}")
    def start_external_receiver(self):
        '''
        This function starts a socket server to connect to the backend endpoint and receive user prompts.
        '''
        self.external_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.external_receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.external_receiver_socket.bind(("127.0.0.1", 65000))
        self.external_receiver_socket.listen(5)  # Start listening for incoming connections
        
        self.external_receiver_thread = threading.Thread(target=self.receive_external_data)
        self.external_receiver_thread.daemon = True
        self.external_receiver_thread.start()

    def receive_external_data(self):
        '''
        This function handles the receipt of prompts from the backend endpoint by accepting connections.
        '''
        print("Listening for external data on port 65000 for user prompt...")
        while self.running:
            try:
                client_socket, addr = self.external_receiver_socket.accept()  # Accept an incoming connection
                print(f"Connection accepted from {addr}")
                data = client_socket.recv(2048).decode()  # Receive data from the connected client

                if data:
                    print(f"\nReceived external data: {data}")
                    self.prompt_queue.put({'message': data, 'sender': 'Endpoint-65000'})

                client_socket.close()  # Close the client connection after handling
            except ConnectionResetError:
                print("Connection to the external data sender lost.")
                break
            except Exception as e:
                print(f"Error receiving external data: {e}")

    def close(self):
        self.running = False
        self.broadcast_socket.close()
        self.listen_socket.close()
        self.external_receiver_socket.close()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                              Database
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_history():
    """
    This function queries supabase and gets the last five data points, and returns a list of the required parameters, after filtering it.
    """
    response = supabase.table('History').select("*").order('id', desc=True).limit(5).execute().data
    
    keys_to_keep = {'SysBool', 'M_func', 'Prompt'}
    filtered_data = [{key: dos[key] for key in dos if key in keys_to_keep} for dos in response]    
    return response
    
def add_history(name, system_boolean, prompt):
    """
    This function is to be called whenever the broadcaster receives data from any node. When it recieves data, it means the node must've fired up. 
    It will extract the relevant data from the node and add that to the database for further history implementation.

    This is to be called after querying the database, so that the current input is not regarded as history.
    """
    Info = {'SysBool': f"{system_boolean}", 'M_func': f"{function_dict.get(name)}", 'Prompt': f"{prompt}"}
    response = supabase.table('History').insert(Info).execute()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     comms with breakout and start
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_prompt(broadcaster):
    '''
    This function essentially 
    '''
    try:
        user_message = broadcaster.prompt_queue.get(timeout = 5)
        return user_message['message']  
    except Exception as e:
        print(e)
        return f'An exception occurred: {e}'

if __name__ == "__main__":

    BROADCAST_PORTS = [5000+i for i in range(1,4)]  # Ports to broadcast to
    LISTEN_PORT = 5000  # Port to listen on
    broadcaster = BroadcasterListener(BROADCAST_PORTS, LISTEN_PORT)
    broadcaster.start_external_receiver()                               # listening for data from the endpoint

    try:
        while True:
            if not broadcaster.prompt_queue.empty():
                prompt = broadcaster.prompt_queue.get()
                print(f"Broadcasting received prompt: {prompt['message']}")
                if prompt['message'].lower() == 'quit':
                    break
                history = get_history()
                broadcaster.broadcast_message(prompt['message'], history)
            try:
                messages = broadcaster.message_queue.get(timeout=5)          # Waits up to 5 seconds for a message from the models
                system_boolean = messages['sysbool']
                name = f"client_{messages['sender'].split('-')[1]}"
                add_history(name, system_boolean, prompt)
                print('added history')
            except queue.Empty:
                # Timeout after 5 seconds, continue if no message was received
                print('No message received within 5 seconds. Message queue is empty.')

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        broadcaster.close()