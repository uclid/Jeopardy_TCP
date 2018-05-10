import socket
import json

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('localhost', 9999))

# send some data (in this case a HTTP GET request)
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client.send(message.encode())

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print (response.decode())

endGame = False
while not endGame:
    #keep checking for end, keep waiting
    #client.send(message.encode()) 
    response = client.recv(4096)
    print (response.decode())
    if response.decode() == 'END':
        print ('Game has ended!')
        endGame = True
