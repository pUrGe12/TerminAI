from concurrent.futures import ThreadPoolExecutor  # For parallel message sending
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
        self.json_queue = queue.Queue()
        self.sysbool_queue = queue.Queue()

        # UDP socket for receiving messages
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_socket.bind(('127.0.0.1', self.port))

        # UDP socket for sending messages
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Start threads for listening and processing messages
        self.processor_thread = threading.Thread(target=self.process_and_send)
        self.processor_thread.daemon = True
        self.processor_thread.start()

    def listen(self):
        print(f"Listening for messages on port {self.port}...")
        while self.running:
            try:
                data, addr = self.receive_socket.recvfrom(1024)
                received_data = json.loads(data.decode('utf-8'))
                print(f"\nReceived message from {addr}")
                print(f"\nJson value: {received_data['json_value']}")
                print(f"\nSystem_bool: {received_data['system_bool']}")
                print(f"\nSender: {received_data['sender']}")
                print(f"\nwork summary: {received_data['work_summary']}")
                print(f"\nPrompt: {received_data['prompt']}")

                # Put data into queues for processing
                self.prompt_queue.put(received_data['prompt'])
                self.model_queue.put(f"client_{received_data['sender'].split('_')[1]}")
                self.json_queue.put(received_data['json_value'])
                self.sysbool_queue.put(received_data['system_bool'])

            except json.JSONDecodeError:
                print(f"\nReceived malformed data from {addr}")
            except Exception as e:
                if self.running:
                    print(f"\nError while listening: {e}")

    def process_and_send(self):
        """
        Checks the sysbool value and sends the message to the relevant set of ports.
        """
        while self.running:
            try:
                if not self.prompt_queue.empty() and not self.sysbool_queue.empty():
                    prompt = self.prompt_queue.get()
                    sysbool = self.sysbool_queue.get()  # This is a real boolean

                    # Define ports based on sysbool value
                    if sysbool == True:
                        target_ports = [65011, 65012, 65013]
                    else:
                        target_ports = [65014, 65015]

                    # Send message to all relevant ports using ThreadPoolExecutor for parallel sending
                    with ThreadPoolExecutor(max_workers=len(target_ports)) as executor:
                        for port in target_ports:
                            executor.submit(self.send_to_port, prompt, port)

            except Exception as e:
                print(f"\nError in processing or sending: {e}")

    def send_to_port(self, message, port):
        """
        Send the message to the specified port.
        """
        data = {
            'prompt': message,
            'sender': f'Listener-{self.port}'
        }
        encoded_data = json.dumps(data).encode('utf-8')
        try:
            self.send_socket.sendto(encoded_data, ('127.0.0.1', port))
            print(f"\nSent message to port {port}: {message}")
        except Exception as e:
            print(f"\nError sending to port {port}: {e}")

    def close(self):
        self.running = False
        self.receive_socket.close()
        self.send_socket.close()
        print("Listener has been shut down.")

if __name__ == "__main__":
    listener = Listener65032()
    try:
        listener.listen()
    except KeyboardInterrupt:
        print("\nShutting down listener...")
    finally:
        listener.close()
