##Client

import socket
import sys
import json
import time
import signal

timeout = None

#to timeout the input in case of ringing and answering
def stdinWait(text, default, time = 5, timeoutDisplay = None, **kwargs):
    signal.signal(signal.SIGALRM, interrupt)
    signal.alarm(time) # sets timeout
    global timeout
    try:
        inp = input(text)
        signal.alarm(0)
        timeout = False
    except (KeyboardInterrupt):
        printInterrupt = kwargs.get("printInterrupt", True)
        if printInterrupt:
            print ("Keyboard interrupt")
        timeout = True # Do this so you don't mistakenly get input when there is none
        inp = default
    except:
        timeout = True
        if not timeoutDisplay is None:
            print (timeoutDisplay)
        signal.alarm(0)
        inp = default
    return inp

def interrupt(signum, frame):
    raise Exception("")
#for windows
#vars
connected = False
state = 0
rounds = 1
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
        print("ROUND ", rounds)
        data = client_socket.recv(1024) 
        cmd = json.loads(data.decode()) #we now only expect json
        print("The available categories are {}".format(SM_NEW_GAME["categories"]))
        print("Each categories have {} questions".format(SM_NEW_GAME["ques_in_categories"]))
        if(cmd["selected_player"] == player_id):
            print("You are selected!!")
            category = int(input('Please select a category (0,1,2..) in order they are displayed: '))
            CM_CATEGORY = {'player_id': player_id,'category': category}
            message = json.dumps(CM_CATEGORY)
            client_socket.send(message.encode())            
        else:
            print("Player {} is selecting a category...".format(cmd["selected_player"]))
        state = 2
    elif(state == 2): #select category
        data = client_socket.recv(1024) 
        cmd = json.loads(data.decode()) #we now only expect json
        print("Category selected is {}.".format(SM_NEW_GAME["categories"][cmd["category"]]))
        state = 3
    elif(state == 3): #display question and ring
        data = client_socket.recv(1024) 
        cmd = json.loads(data.decode()) #we now only expect json
        print("Your question is {}.".format([cmd["question"]]))
        ring = int(stdinWait('Please press 1 and enter to ring...', 100))
        if(ring == 1):
            CM_RING = {'ring_player_id': player_id}
            message = json.dumps(CM_RING)
            client_socket.send(message.encode())
        elif(ring == 100):
            CM_RING = {'ring_player_id': ring}
            print("I did not ring")
            message = json.dumps(CM_RING)
            client_socket.send(message.encode())            
        else:
            print("Wrong buzzer press, you missed out")
        state = 4
    elif(state == 4): #allow answering question, after ring is correct
        data = client_socket.recv(1024)
        cmd = json.loads(data.decode()) #we now only expect json
        if(cmd["player_id"] == 100):
            print("You did not ring!!")
        elif(cmd["player_id"] == player_id):
            print("You can answer!!")
            answer = stdinWait('Please enter your answer: ', "")
            CM_ANSWER = {'player_id': player_id,'answer': answer}
            message = json.dumps(CM_ANSWER)
            client_socket.send(message.encode())           
        else:
            print("Player {} is answering...".format(cmd["player_id"]))
        state = 5
    elif(state == 5): #answer shown
        data = client_socket.recv(1024)
        cmd = json.loads(data.decode()) #we now only expect json
        if(cmd["correct_answer"] == cmd["client_answer"]):
            message = "correctly"
        else:
            message = "incorrectly"
        print("Correct answer is {}\n Player answered {} with {}".format(cmd["correct_answer"], message, cmd["client_answer"]))
        state = 6
    elif(state == 6): #round ended
        data = client_socket.recv(1024)
        cmd = json.loads(data.decode())
        print("---------------------------------------------------")
        print("Scores after Round {}".format(rounds))
        print("---------------------------------------------------")
        print("{}\t\t\t\t{}".format(SM_NEW_GAME['player_names'][0],SM_NEW_GAME['player_names'][1]))
        print("{}\t\t\t\t{}".format(cmd["scores"][0],cmd["scores"][1]))
        print("---------------------------------------------------")
        rounds = rounds + 1
        if(rounds<4):
            state = 1
        else:
            state = 7        
    elif(state == 7): #end game
        data = client_socket.recv(1024)
        cmd = json.loads(data.decode())
        print(cmd["end"])
        state = 8
