import socket
import threading
import time
import json
import sys
from queue import Queue
import re
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
from Ex_address import prompt_dict, prompt_init_dict

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent / '.env')
API_KEY = str(os.getenv("API_KEY")).strip()

NAME = 'client_5002'

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

model_init = genai.GenerativeModel('gemini-pro')
chat_init = model_init.start_chat(history=[])

class ReceiverSender:
    '''
    It has two running queues, one for messages and one for the history. When it receives the history information from the broadcaster, it adds the list in this queue.
    We use queues cause its faster
    '''

    def __init__(self, listen_port, broadcaster_port):
        self.listen_port = listen_port
        self.broadcaster_port = broadcaster_port
        self.running = True
        self.message_queue = Queue()                # This is holding the current prompts
        self.history_queue = Queue()                # This is holding the history as a list
        
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
    
    def send_message(self, work_summary):
        """
        send the feedback to the sequencer. The feedback includes
        1. system boolean value
        2. Model name (or the sender)
        3. work summary

        The prompt is already present with the sequencer.
        """
        data = {
            'sysbool': True,                            # If this code sends data, then it must have been a system level operation!
            'sender': f'Node-{self.listen_port}',       # This essentially gives the model function
            'work_summary': work_summary                # A short 20 word summary on what the user asked and what the model generated
        }
        encoded_data = json.dumps(data).encode('utf-8')
        try:
            self.send_socket.sendto(encoded_data, ('255.255.255.255', self.broadcaster_port))
            print(f"\nSent feedback to broadcaster: {encoded_data}")
        except Exception as e:
            print(f"\nError sending message: {e}")

    def send_to_GPT_breakout(self, json_value, user_prompt, work_summary, listener_port=65032):
        """
        Send message to breakout GPT via port 65032. The things we want to send are

        1. json value
        2. model name (to figure out what it was trying to do)
        3. work_summary
        4. user_prompt

        We call this only if the M_init gives a yes.
        """
        data = {
            'json_value': json_value,
            'system_bool': True,                                # If this code sends data, then it must have been a system level operation!
            'sender': NAME,                                     # The model name is important because it determines which ports to broadcast further to
            'prompt': user_prompt,                              # This is the user's prompt, still being carried around
            'work_summary': work_summary                        # The work summary
        }
        encoded_data = json.dumps(data).encode('utf-8')
        try:
            self.send_socket.sendto(encoded_data, ('127.0.0.1', listener_port))
            print(f"\nSent to GPT breakout on port {listener_port}: {encoded_data}")
        except Exception as e:
            print(f"\nError sending to additional listener: {e}")

    def print_received_message(self, addr, received_data):
        """
        Print received message and add it to the queue, this is from the sequencer.
        """
        print(f"\nReceived broadcast from {addr}: {received_data['current_prompt']}")
        print(f"Sender: {received_data['sender']}")
        print(f"History: {received_data['history']}")
        
        # Don't process messages from ourselves
        if received_data['sender'] != f'Node-{self.listen_port}':
            self.message_queue.put(received_data['current_prompt'])         # Adding the current prompt here.
            self.history_queue.put(received_data['history'])                # Adding the history here.
    
    def listen_for_broadcasts(self):
        """Listen for incoming broadcast messages"""
        print(f"Listening for broadcasts on port {self.listen_port}...")
        while self.running:
            try:
                data, addr = self.receive_socket.recvfrom(4096)
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

def M_init(user_prompt, history):
    '''
    This model is checking if this file is even required. Its very basic, outputs a True or a False, depending on whether the file is needed.
    '''
    prompt_init = prompt_init_dict.get(f"{NAME}_init") + f"""
                    This is the history: {history}
                    This is the user's prompt: {user_prompt}
    """

    try:
        output_init = ""
        response_init = chat_init.send_message(prompt_init, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })

        for chunk in response_init:
            if chunk.text:
                output_init += str(chunk.text)

        if "yes" in output_init.lower():                        # This will give just one boolean value
            return True
        else:
            return False
    except Exception as e:
        return f"error occured {e}"

def GPT_response(user_prompt, history):
    prompt = prompt_dict.get(NAME) + f"""
                    This is the history: {history}
                    This is the user's prompt: {user_prompt}
                """
    try:
        output = ''
        response = chat.send_message(prompt, stream=True, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })
        for chunk in response:
            if chunk.text:
                output += str(chunk.text)

        # parse the output for the json and work summary etc.

        json_list = re.findall('@@@json.*@@@', output, re.DOTALL)
        json_val = re.findall("{.*}", json_list[0].strip(), re.DOTALL)[0].strip() # getting a nice normal string here
        work_summary_match = re.search(r"\$\$\$summary\s*(.*?)\s*\$\$\$", output, re.DOTALL)
        if work_summary_match:
            work_summary = work_summary_match.group(1).strip() # putting an else condition, even though I am sure there must be a match
        else:
            work_summary = 'Something went wrong'

        return (json_val, work_summary)

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return 'Try again'

if __name__ == "__main__":
    LISTEN_PORT = 5002  # listen for broadcasts
    BROADCASTER_PORT = 5000 
    
    receiver = ReceiverSender(LISTEN_PORT, BROADCASTER_PORT)
    try:
        while True:
            if not receiver.message_queue.empty():
                user_prompt = receiver.message_queue.get()
                history = receiver.history_queue.get()

                answer = M_init(user_prompt, history)

                if answer == True:
                    ''' First check if the current model is required for the prompt '''
                    (json_val, work_summary) = GPT_response(user_prompt, history)

                    # Now run the GPT model to generate the json

                    receiver.send_message(work_summary)                                              # sending feedback
                    receiver.send_to_GPT_breakout(json_val, user_prompt, work_summary)               # sending to GPT breakout    
            time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        receiver.close()