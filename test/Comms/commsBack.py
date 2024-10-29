import socket

host = "127.0.0.1"
port = 64920

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((host,port))

server_socket.listen()

print('listening...')

conn, addr = server_socket.accept()
print(f'connected to by {addr}')

try:
    while True:
        data = conn.recv(2048) 
        if not data:
            break
        print("Received message:", data.decode())
finally:
    conn.close()
    server_socket.close()

