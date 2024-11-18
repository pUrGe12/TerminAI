import socket
import threading
import time
import json
import queue
from supabase import create_client, Client                                        # For database adding and pulling
from Ex_address import function_dict                                              # For getting information on the models, to add to database

import os
from dotenv import load_dotenv
from pathlib import Path

# Supabase API setup

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / '.env')

url: str = str(os.getenv("SUPABASE_URL")).strip()
key: str = str(os.getenv("SUPABASE_KEY")).strip()

supabase: Client = create_client(url, key)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                      The broadcasting class
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

class BroadcasterListener:
    '''
    This class creates a broadcast instance that asynchronously sends data to multiple models,
    while a daemon listens for incoming connections on a different thread.
    
    This uses a queue to push the received data into it. 
    '''

    def __init__(self, broadcast_ports, listen_port):
        '''
            We've used two queues:
            1. To get feedback from the models
            2. To use the user's current prompt

            We're not using a queue for the history, there is a function that just pulls and does that, because duh, we're not receiving it from any other socket.

            In this broadcaster we've started a socket for broadcasting and one for listening, that is in a different thread. 
            We really don't have to use different cores for broadcasting cause its only 6 models we have to do it to, its small so the small delays will not make much of a difference.
        '''

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
    
    def broadcast_message(self, current_prompt, history):
        """
        Broadcasts the prompt and history list to all models in the extraction layer.

        Here we are broadcasting the current prompt and the history to all the models. We'll also put the sender, its important because its being used to ensure that the listeners
        (the clients) are not listening to their own messages!

        We encode and send it to the broadcast ports. This is a predefined list, we can always add more into it.
        """
        
        assert isinstance(history, list), 'history is wrongly formatted, it must be a list'

        data = {
            'current_prompt': current_prompt,
            'history': history,
            'sender': f'Sequencer-{self.listen_port}'         # This is necessary
        }
        encoded_data = json.dumps(data).encode('utf-8')
        
        try:
            for port in self.broadcast_ports:
                self.broadcast_socket.sendto(encoded_data, ('255.255.255.255', port))
                print(f"\nBroadcasted to port {port}: {encoded_data}")
        except Exception as e:
            print(f"\nError broadcasting message: {e}")

    def print_received_message(self, addr, received_data):
        """
        Pretty-printing of the received message and adding it to the queue for external access. This is the one received from the extraction layer.
        """
        print(f"\nReceived from {addr}")
        print(f"Sender: {received_data['sender']}")
        print(f"sysbool: {received_data['sysbool']}")
        print(f"work_summary: {received_data['work_summary']}")
        print("\nEnter message to broadcast (or 'quit' to exit): ", end='', flush=True)
        
        self.message_queue.put(received_data)

    def listen_for_messages(self):
        """
        This is to listen for incoming feedback from the extraction layer. 
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
        This function handles the receiving of prompts from the backend endpoint by accepting connections. This is the only comms it needs with the endpoint.
        
        We're already getting the prompt from the endpoint
        '''

        print("Listening for external data on port 65000 for user prompt...")
        while self.running:

            try:
                client_socket, addr = self.external_receiver_socket.accept()  # Accept an incoming connection
                print(f"Connection accepted from {addr}")
                data = client_socket.recv(2048).decode()  

                if data:
                    print(f"\nReceived external data: {data}")
                    self.prompt_queue.put({'prompt': data, 'sender': 'Endpoint-65000'})             # Adding the current prompt that we recieved from the endpoint to the prompt_queue

                client_socket.close()

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

def get_history(n):
    """
    This function queries supabase and gets the last n data points, and returns a list of the required parameters, after filtering it. This is done from version 2.

    n -> the number of entries you want. I have kept it to be usually at 5.
    """
    response = supabase.table('History_v2').select("*").order('id', desc=True).limit(n).execute().data      # Take the last n
    
    keys_to_keep = {'system_boolean', 'ex_model_function', 'user_prompt', 'ex_work_summary'}
    filtered_data = [{key: dos[key] for key in dos if key in keys_to_keep} for dos in response]    
    return response
    
def add_history(name, system_boolean, prompt, ex_work_summary):
    """
    This function will add the necessary data it recieved from the models to the database. 
    
    Adding it to version 2.
    """

    Info = {'system_boolean': f"{system_boolean}", 'ex_model_function': f"{function_dict.get(name)}", 'user_prompt': f"{prompt}", "ex_work_summary": f"{ex_work_summary}"}
    response = supabase.table('History_v2').insert(Info).execute()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                     comms with breakout and start
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    BROADCAST_PORTS = [5000+i for i in range(1,7)]                           # Ports to broadcast to, 5001 to 5006 --> all the extraction models
    LISTEN_PORT = 5000  # Port to listen on
    broadcaster = BroadcasterListener(BROADCAST_PORTS, LISTEN_PORT)
    broadcaster.start_external_receiver()                                    # listening for data from the endpoint

    try:
        while True:
            if not broadcaster.prompt_queue.empty():
                try:
                    prompt = broadcaster.prompt_queue.get(timeout = 5)          # Waits up to 5 seconds for the prompt from the endpoint

                    print(f"Broadcasting received prompt: {prompt['prompt']}")
                    
                    if prompt['prompt'].lower() == 'quit':
                        break
                    
                    history = get_history(3)
                    broadcaster.broadcast_message(prompt['prompt'], history)
                except queue.Empty:
                    print('No prompt recieved till now. It has been 5 seconds')

            try:
                messages = broadcaster.message_queue.get(timeout=5)          # Waits up to 5 seconds for the feedback from the models
                
                system_boolean = messages['sysbool']
                name = f"client_{messages['sender'].split('-')[1]}"
                work_summary = messages['work_summary']
                
                add_history(name, system_boolean, prompt, work_summary)
                print('added history')
            
            except queue.Empty:
                # Timeout after 5 seconds, continue if no message was received
                print('No feedback received till now. It has been 5 seconds')

    except KeyboardInterrupt:
        print("\nShutting down...")
    
    finally:
        broadcaster.close()