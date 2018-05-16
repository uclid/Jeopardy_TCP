import socket
import json

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('localhost', 9999))

# send CM_SUBSCRIBE in JOINING_GAME state
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client.send(message.encode())

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

#print (response.decode())
#request = client_socket.recv(1024)
server_message = json.loads(response.decode())
print ('Received {}'.format(server_message))
player_id = (server_message['player_names']).index(name) + 1 
print ('Player ID {}'.format(player_id))

#send CM_Category
response1 = client.recv(4096)
server_message1 = json.loads(response1.decode())
print(server_message1)
selected_id = (server_message1['selected_player'])
print ('Player {} is selected for this round'.format(selected_id))
if selected_id == player_id:
    category_id = input('Your Category: ')
    CM_CATEGORY = {'Category ID': category_id, 'Player ID': player_id}
    message1 = json.dumps(CM_CATEGORY)
    client.send(message1.encode())

response2 = client.recv(4096)
server_message2 = json.loads(response2.decode())
selected_question = (server_message2['selected_question'])
print ('Question selected for this round is {}'.format(selected_question))   


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

endGame = False
while not endGame:
    #keep checking for end, keep waiting
    #client.send(message.encode()) 
    response = client.recv(4096)
    print (response.decode())
    if response.decode() == 'END':
        print ('Game has ended!')
        endGame = True
