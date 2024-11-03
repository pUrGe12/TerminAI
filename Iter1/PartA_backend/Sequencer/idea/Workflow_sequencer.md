# The overview

Here is the exact explanation, point to point details, of what is happening with the sequencer.

:x: It has a socket connection with the breakout. It recieves user's prompt from there. It only needs to receive from the breakout and not send anything back.

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
		                if self.running:
		                    print(f"\nError while listening: {e}")

		    def close(self):
		        self.running = False
		        self.broadcast_socket.close()
		        self.listen_socket.close()


Here, 

- We establish a message queue, thread the `listen_for_message()` method and create socket objects to use later.
- The `broadcast_message()` method takes in the prompt and the history and sends it over to everyone.

The history that we pull from supabase has things that we don't need often, so, we'll just pass the ones that are required and important. This we filter using the `get_history()` function,

		def get_history():
		    response = supabase.table('History').select("*").order('id', desc=True).limit(5).execute().data
		    keys_to_keep = {'SysBool', 'M_func', 'Prompt'}
		    filtered_data = [{key: dos[key] for key in dos if key in keys_to_keep} for dos in response]    
		    return response

- It then establishes the listen_for_message() method, trying to listen from any port, on the port 5000. 

> [!Note]
> Ensure that the port you're using are not already used by others!

## Understanding main

This is the main code, 

		if __name__ == "__main__":
			BROADCAST_PORTS = [5000+i for i in range(1,4)]  # Ports to broadcast to, we can increase this to how much ever we want.
			LISTEN_PORT = 5000
			broadcaster = BroadcasterListener(BROADCAST_PORTS, LISTEN_PORT)
			try:
			    while True:
			        history, prompt = get_history(), get_prompt()
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

This is establishing the ports we need to broadcast to first, then the port to listen on.

- We keep querying history and getting the prompt until the prompt is `quit`. This is kind of equivalent to `ctrl+d` in the actual terminal. 
- Then we create an instance of the broadcaster class.

Now we check if the message_queue is empty of not. Note that we're only adding anything to the message_queue in the `print_received_message()` method. So, if it has atleast one message, this block of code executes.

After `print_received_message()` runs and the queue is processed in the main loop using `.get()`, the queue will be empty until the listen_for_messages() thread receives and processes a new message. If no new messages are received, the queue will remain empty, and `if not broadcaster.message_queue.empty()` will evaluate to `False`.

The queue will at max have only one element at a time. Because, as soon as it has one, the main loop will `get` that and pop it. That is how we implement history.	

---
