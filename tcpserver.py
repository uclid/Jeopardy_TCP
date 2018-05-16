import socket
import threading
import json
import random

bind_ip = 'localhost'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections
client_list = []

MIN_PLAYERS = 3

game_flag= 0
round_flag = 0

player_names = []
num_categories = 5
categories = ['Movies','Sportsmen','Capital Cities','US History','Artists']
ques_in_categories = 2
questions = [['Best Oscar Movie 2017','Highest Grossing Movie of all time'],
             ['World Cup 2018 is here','Current NBA Champions'],
             ['Capital of Nepal','Capital of Bangladesh'],
             ['The First State','The Last State'],
             ['Painted Monalisa','Composed Fur Elise']]
''' 
answers =
[['moonlight','avatar'],
['russia','golden state warriors'],
['kathmandu','dhaka'],
['delaware','hawaii'],
['da vinci','beethoven']]
'''
def_timeout = 5000 #3 seconds

print ('Listening on {}:{}'.format(bind_ip, bind_port))


def handle_client_connection(client_socket):
    #collect subscriptions
    request = client_socket.recv(1024)
    client_message = json.loads(request.decode())
    print ('Received {}'.format(client_message['name']))
    
    player_names.append(client_message['name'])
    num_players = threading.activeCount() -1
      
    #game in progress 
    while len(player_names) < MIN_PLAYERS:
        #keep waiting until all have input their names
        2==2
    if game_flag == 0:
        broadcast_game(num_players)
    
    #round in progress
    if round_flag == 0:
        broadcast_round(num_players)
    
    #category_selected (wait until a category is picked by the selected player)
    request = client_socket.recv(1024)
    client_message = json.loads(request.decode())
    print ('Received from player {} the category {}'.format(client_message['player_id'],client_message['category_id'])) #getting category from client 
    category = client_message['category_id']
    
    selected_question = random.randint(1,2)
    SM_QUESTION = {"selected_question" : questions[category][selected_question]}
    
    message = json.dumps(SM_QUESTION)
    client_socket.send(message.encode())  
    
    #waiting for ring
    ring = False
    
    
    
    #wait for cm answer
    
    #end of round
    
    #end game
    client_socket.send(b'END')
    client_socket.close()

def broadcast_game(num_players):
    SM_NEW_GAME = { 'num_players' : num_players,
                    'player_names' : player_names,
                'num categories' : num_categories,
                'categories' : categories,
                'ques_in_categories' : ques_in_categories,
                'def_timeout' : def_timeout }

    message = json.dumps(SM_NEW_GAME)
    
    for clients in client_list:
        send_msg(client, message.encode())
    game_flag = 1

def broadcast_round(num_players):
    selected_player = random.randint(1,num_players+1)
    SM_NEW_ROUND = {"selected_player" : selected_player}
    
    message = json.dumps(SM_NEW_ROUND)
    
    for clients in client_list:
        clients.send(message.encode())  
    round_flag = 1

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def remove(connection):
    if connection in client_list:
        client_list.remove(connection)

while True:
    if((threading.activeCount() - 1) < MIN_PLAYERS):
        client_sock, address = server.accept()
        client_list.append(client_sock)
        print ('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        print ('Number of active clients: {}'.format(threading.activeCount()))
        client_handler.start()
