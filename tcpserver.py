import socket
import threading
import json

bind_ip = 'localhost'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print ('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    #collect subscriptions
    request = client_socket.recv(1024)
    client_message = json.loads(request.decode())
    print ('Received {}'.format(client_message['name']))
    #game in progress
    client_socket.send(b'ACK!')
    
    #end game
    client_socket.send(b'END')
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print ('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    print ('Number of active clients: {}'.format(threading.activeCount()))
    client_handler.start()
