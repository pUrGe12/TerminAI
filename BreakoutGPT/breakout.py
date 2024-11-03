from Ex_address import function_dict
import socket
import json
import queue
import threading

class Listener65032:
    def __init__(self, port=65032):
        self.port = port
        self.running = True
        self.prompt_queue = queue.Queue()
        self.model_queue = queue.Queue()
        self.sysbool_queue = queue.Queue()

        # UDP socket for receiving messages
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(('127.0.0.1', self.port))

        # UDP socket for sending messages
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Start a thread for processing messages
        self.processor_thread = threading.Thread(target=self.process_output)
        self.processor_thread.daemon = True
        self.processor_thread.start()

    def listen(self):
        print(f"Listening for messages on port {self.port}...")
        while self.running:
            try:
                data, addr = self.receive_socket.recvfrom(1024)
                received_data = json.loads(data.decode('utf-8'))
                print(f"\nReceived message from {addr}: {received_data['message']}")
                print(f"Sender: {received_data['sender']}")
                print(f"Sysbool: {received_data['sysbool']}")
                print(f"Prompt: {received_data['prompt']}")

                self.prompt_queue.put(received_data['prompt'])
                self.model_queue.put(f"client_{received_data['sender'].split('-')[1]}")
                self.sysbool_queue.put(received_data['sysbool'])

            except json.JSONDecodeError:
                print(f"\nReceived malformed data from {addr}")
            except Exception as e:
                if self.running:
                    print(f"\nError while listening: {e}")

    def process_output(self):
        """
        This is the parent function. It processes the data recieved and sends it to the relevant port (that is, the relevant GPT model)

        Modify the different processing functions, add if necessary, to suit the needs.
        """
        while self.running:
            if not self.message_queue.empty():
                prompt = self.prompt_queue.get()
                model = self.model_queue.get()
                sysbool = self.sysbool_queue.get()

                m_func = function_dict.get(model_queue)

                processed_message = self.process_message(prompt, sysbool, m_func)
                target_port = self.determine_port(processed_message)
                
                if target_port:
                    self.send_to_port(processed_message, received_data['sysbool'], target_port)

    def process_message(self, user_prompt, sysbool, model_function):
        '''
        Process the message, based on the sysbool value, prompt and the model function.
        '''
        pass

    def determine_port(self, processed_message):
        '''
        Which port to send based on the processed message.
        '''
        pass

    def send_to_port(self, message, sysbool, port):
        """
        Send the processed message to the specified port
        """
        data = {
            'message': message,
            'sysbool': sysbool,
            'sender': f'Listener-{self.port}'
        }
        encoded_data = json.dumps(data).encode('utf-8')
        try:
            self.send_socket.sendto(encoded_data, ('127.0.0.1', port))
            print(f"\nSent processed message to port {port}: {message}")
        except Exception as e:
            print(f"\nError sending to port {port}: {e}")

    def close(self):
        self.running = False
        self.receive_socket.close()
        self.send_socket.close()

if __name__ == "__main__":
    listener = Listener65032()
    try:
        listener.listen()
    except KeyboardInterrupt:
        print("\nShutting down listener...")
    finally:
        listener.close()
