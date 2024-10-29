# this is the client - the terminal which sends data

import socket

host = '127.0.0.1' 
port = 64920       

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((host, port))
print("Connected to the server")

try:
    while True:
        try:
            message = input("Enter message to send: ")
            client_socket.sendall(message.encode()) 
            if message.lower() == 'exit':
                print("Exiting...")
                break
        except (KeyboardInterrupt, EOFError):
            # If the user presses Ctrl+c or Ctrl+d
            print("\nDetected interrupt or EOF, closing connection...")
            break
finally:
    client_socket.close()
    print("Connection closed.")