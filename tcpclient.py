import socket
import json

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('localhost', 9999))

# send CM_SUBSCRIBE
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client.send(message.encode())

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print (response.decode())

#send CM_Category
category_id = input('Your Category: ')
player_id = input('Your Player id:')
CM_CATEGORY = {'Category ID': category_id, 'Player ID': player_id}
message1 = json.dumps(CM_CATEGORY)
client.send(message1.encode())

#send CM_RING
player_id = input('Your Player id:')
CM_RING = {'Player ID': player_id}
message2 = json.dumps(CM_RING)
client.send(message2.encode())

#send CM_ANSWER
player_answer = input('Type in your answer:')
CM_ANSWER = {'Player Answer': player_answer}
message3 = json.dumps(CM_RING)
client.send(message3.encode())

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

endGame = False
while not endGame:
    #keep checking for end, keep waiting
    #client.send(message.encode()) 
    response = client.recv(4096)
    print (response.decode())
    if response.decode() == 'END':
        print ('Game has ended!')
        endGame = True
