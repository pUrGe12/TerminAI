import socket
import threading
import time
import json
import sys
from queue import Queue
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
from address import prompt_dict

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                           GPT initializations
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

NAME = 'client_5001'

API_KEY = "AIzaSyDgtJZg8o9fYUlJm9xeYNkRwzQ2nbZiHQI"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                                         Receiver and Sender class
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

class ReceiverSender:
    '''
    It has two running queues, one for messages and one for the history. When it receives the history information from the broadcaster, it adds the list in this queue.
    We use queues cause its faster
    '''

    def __init__(self, listen_port, broadcaster_port):
        self.listen_port = listen_port
        self.broadcaster_port = broadcaster_port
        self.running = True
        self.message_queue = Queue()
        self.history_queue = Queue()
        
        # UDP socket for receiving broadcasts
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(('', self.listen_port))
        
        # UDP socket for sending messages
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # listener thread
        self.listener_thread = threading.Thread(target=self.listen_for_broadcasts)
        self.listener_thread.daemon = True
        self.listener_thread.start()
    
    def send_message(self, message, sysbool):
        """ send message to the broadcaster """
        data = {
            'message': message,
            'sysbool': sysbool,
            'timestamp': time.strftime('%H:%M:%S'),
            'sender': f'Node-{self.listen_port}'
        }
        encoded_data = json.dumps(data).encode('utf-8')
        try:
            self.send_socket.sendto(encoded_data, ('255.255.255.255', self.broadcaster_port))
            print(f"\nSent to broadcaster: {message}")
        except Exception as e:
            print(f"\nError sending message: {e}")

    def print_received_message(self, addr, received_data):
        """Print received message and add it to the queue"""
        print(f"\nReceived broadcast from {addr}: {received_data['message']}")
        print(f"Timestamp: {received_data['timestamp']}")
        print(f"Sender: {received_data['sender']}")
        print(f"History: {received_data['history']}")
        
        # Don't process messages from ourselves
        if received_data['sender'] != f'Node-{self.listen_port}':
            self.message_queue.put(received_data['message'])
            self.history_queue.put(received_data['history'])
    
    def listen_for_broadcasts(self):
        """Listen for incoming broadcast messages"""
        print(f"Listening for broadcasts on port {self.listen_port}...")
        while self.running:
            try:
                data, addr = self.receive_socket.recvfrom(1024)
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
                if self.running:
                    print(f"\nError while listening: {e}")
    
    def close(self):
        self.running = False
        self.receive_socket.close()
        self.send_socket.close()

def GPT_response(prompt, history):
    prompt_init = prompt_dict.get(NAME) + f"""
                    This is the history: {history}
                    This is the prompt: {prompt}
                """

    try:
        output_init = ''
        response_init = chat.send_message(prompt_init, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })
        for chunk in response_init:
            if chunk.text:
                output_init += str(chunk.text)
        sysbool = output_init.strip().split(',')[0].split(':')[1].strip()
        answer = output_init.strip().split(',')[1].split(':')[1].strip()
        
        return (sysbool, answer)

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return 'Try again'

if __name__ == "__main__":
    LISTEN_PORT = 5001  # listen for broadcasts
    BROADCASTER_PORT = 5000 
    
    receiver = ReceiverSender(LISTEN_PORT, BROADCASTER_PORT)
    try:
        while True:
            if not receiver.message_queue.empty():
                received_message = receiver.message_queue.get()
                history = receiver.history_queue.get()
                (sysbool, answer) = GPT_response(received_message, history)
                if "yes" in answer.lower():
                    receiver.send_message(answer, sysbool)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        receiver.close()