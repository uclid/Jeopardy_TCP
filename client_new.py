##Client

import socket
import sys
import json

#vars
connected = False
state = 0
SM_NEW_GAME = {}
player_id = 0

#connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost',8888))
connected = True
#subscribing state
print('Network Jeopardy Game')
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client_socket.send(message.encode())

while connected == True:
    if(state == 0):#game in progress
        #wait for server commands to do things, now we will just display things
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        SM_NEW_GAME = cmd
        
        player_id = (SM_NEW_GAME['player_names']).index(name) + 1 
        print ('Your Player ID is {}'.format(player_id))

        state = 1
    elif(state == 1):#round in progress
        #wait for server commands to do things, now we will just display things
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        print("The available categories are {}".format(SM_NEW_GAME["categories"]))
        print("Each categories have {} questions".format(SM_NEW_GAME["ques_in_categories"]))
        if(cmd["selected_player"] == player_id):
            print("You are selected!!")
            category = int(input('Please select a category (1,2,3..) in order they are displayed: '))
            SM_CATEGORY = {'category': category}
            message = json.dumps(SM_CATEGORY)
            client_socket.send(message.encode())            
        else:
            print("Player {} is selecting a category...".format(cmd["selected_player"]))
        state = 2
    elif(state == 2):
        data = client_socket.recv(1024) 
        #decoded = data.decode()
        #list_message = decoded.split('\n')
        cmd = json.loads(data.decode()) #we now only expect json
        print("Category selected is {}.".format(SM_NEW_GAME["categories"][cmd["category"]]))
        xyz = input("please wait for question...")
