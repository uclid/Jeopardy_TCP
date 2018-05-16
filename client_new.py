##Client

import socket
import sys
import json

#vars
connected = False

#connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost',8888))
connected = True
name = input('Your name: ')
CM_SUBSCRIBE = {'name': name}
message = json.dumps(CM_SUBSCRIBE)
client_socket.send(message.encode())

while connected == True:
    #wait for server commands to do things, now we will just display things
    data = client_socket.recv(1024) 
    #decoded = data.decode()
    #list_message = decoded.split('\n')
    cmd = json.loads(data.decode()) #we now only expect json
    print(cmd)
    '''if(cmd['type'] == 'bet'):
        bet = cmd['value']
        print('betting is: '+bet)
    elif (cmd['type'] == 'result'):        
        print('winner is: '+str(cmd['winner']))
        print('payout is: '+str(cmd['payout']))'''
