# The overview

Here is the exact explanation, point to point details, of what is happening with the sequencer.

:cross:  It has a socket connection with the breakout. It recieves user's prompt from there. It only needs to receive from the breakout and not send anything back.

:heavy_check_mark:  It broadcasts the user's input to all the models, at the same time. :relieved:

:heavy_check_mark:  Establishes a `listener thread` for incoming messages from the models.

**The models have been coded to reply if and only if they satisfy what is being asked. So, for any given prompt, there will only be one reply.** :point_left:

:heavy_check_mark: Before broadcasting the user's input, it adds to it the previous history by pulling it from supabase.

:heavy_check_mark: It receives an output from the model, adds it to the database. The only reason its receiving data from the models is for history implementation.

We could've just added to database using the models, but I didn't want to burden those files. That's about it actually.

# The technical explanation

## Understanding the Broadcast-listener class

> [!Tip]
> Make sure you understand has asynchronous comms happen. Will be useful later as well.

		class BroadcasterListener:
		    def __init__(self, broadcast_ports, listen_port):
		        self.broadcast_ports = broadcast_ports
		        self.listen_port = listen_port
		        self.running = True
		        self.message_queue = queue.Queue()
		        
		        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		        
		        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		        self.listen_socket.bind(('', self.listen_port))
		   
		        self.listener_thread = threading.Thread(target=self.listen_for_messages)
		        self.listener_thread.daemon = True  # Make thread daemon so it exits when main thread exits
		        self.listener_thread.start()
		    
		    def broadcast_message(self, message, history):     
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
		        print(f"\nReceived from {addr}: {received_data['message']}")
		        print(f"Timestamp: {received_data['timestamp']}")
		        print(f"Sender: {received_data['sender']}")
		        print(f"sysbool: {received_data['sysbool']}")
		        print("\nEnter message to broadcast (or 'quit' to exit): ", end='', flush=True)
		        
		        self.message_queue.put(received_data)

		    def listen_for_messages(self):
		       	print(f"Listening for messages on port {self.listen_port}...")
		        while self.running:
		            try:
		                data, addr = self.listen_socket.recvfrom(1024)
		                received_data = json.loads(data.decode('utf-8'))
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

		    def get_received_messages(self):
		        messages = []
		        while not self.message_queue.empty():
		            messages.append(self.message_queue.get())
		        return messages
		    
		    def close(self):
		        self.running = False
		        self.broadcast_socket.close()
		        self.listen_socket.close()
