##Server

import socket, time, sys
import threading
import pprint
import json
import random

TCP_IP = 'localhost'
TCP_PORT = 8888
BUFFER_SIZE = 1024

clientCount = 0
state = 0
client_state = 0
selected_player = 0
selected_question = 0
start_time = time.time()
timed_out = 0

class server():

    def __init__(self):
        self.CLIENTS = []
        self.player_names = []
        self.num_categories = 5
        self.categories = ['Movies','Sports','Capital Cities','US History','Artists']
        self.ques_in_categories = 2
        self.questions = [['Best Oscar Movie 2017','Highest Grossing Movie of all time'],
                     ['World Cup 2018 is here','Current NBA Champions'],
                     ['Capital of Nepal','Capital of Bangladesh'],
                     ['The First State','The Last State'],
                     ['Painted Monalisa','Composed Fur Elise']]
        
        self.answers = [['moonlight','avatar'],
        ['russia','golden state warriors'],
        ['kathmandu','dhaka'],
        ['delaware','hawaii'],
        ['da vinci','beethoven']]
        
        self.def_timeout = 5 #in seconds
        self.SM_CATEGORY = {'category' : -1}
        self.SM_RING_CLIENT = {'player_id' : 0}
        self.SM_ANSWER = {'correct_answer' : "", 'client_answer' : ""}
        self.ring = False


    def startServer(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((TCP_IP,TCP_PORT))
            s.listen(10)
            while 1:
                client_socket, addr = s.accept()
                print ('Client connected with ' + addr[0] + ':' + str(addr[1]))
                global clientCount
                clientCount = clientCount+1
                print (clientCount)
                # register client
                self.CLIENTS.append(client_socket)
                threading.Thread(target=self.playerHandler, args=(client_socket,)).start()
            s.close()
        except socket.error as msg:
            print ('Could Not Start Server Thread. Error Code : ') #+ str(msg[0]) + ' Message ' + msg[1]
            sys.exit()


   #client handler :one of these loops is running for each thread/player   
    def playerHandler(self, client_socket):
        while 1:
            if(client_state == 0):#collect subscriptions
                request = client_socket.recv(BUFFER_SIZE)            
                if not request: 
                    break
                #print ('Data : ' + repr(data) + "\n")
                #data = data.decode("UTF-8")
                # broadcast
                client_message = json.loads(request.decode())
                #print ('Received {}'.format(client_message['name']))            
                #for client in self.CLIENTS:
                    #client.send(data)
                if('name' in client_message.keys()):
                    self.player_names.append(client_message['name'])
                elif('category' in client_message.keys() and (client_message["player_id"] ==  selected_player)):#select category
                    self.SM_CATEGORY['category'] = client_message["category"]
                elif('ring_player_id' in client_message.keys()):
                    if(self.ring == False):
                        self.ring = True
                        self.SM_RING_CLIENT['player_id'] = client_message["ring_player_id"]
                elif('answer' in client_message.keys() and (client_message["player_id"] ==  selected_player)):
                    correct_answer = self.answers[self.SM_CATEGORY["category"]][selected_question]
                    
                    #just return answers, correctness can be checked and displayed at client side
                    self.SM_ANSWER["correct_answer"] = correct_answer
                    self.SM_ANSWER["client_answer"] = client_message["answer"]                    

        # the connection is closed: unregister
        self.CLIENTS.remove(client_socket)
        #client_socket.close() #do we close the socket when the program ends?

    def broadcast(self, message):
        print(message)
        message = json.dumps(message)
        for c in self.CLIENTS:
            c.send(message.encode("utf-8"))

    def _broadcast(self):        
        for sock in self.CLIENTS:           
            try :
                self._send(sock)
            except socket.error:                
                sock.close()  # closing the socket connection
                self.CLIENTS.remove(sock)  # removing the socket from the active connections list

    def _send(self, sock):        
        # Packs the message with 4 leading bytes representing the message length
        #msg = struct.pack('>I', len(msg)) + msg
        # Sends the packed message
        sock.send(bytes('{"sample": "test"}', 'UTF-8'))


if __name__ == '__main__':
    s = server() #create new server listening for connections
    threading.Thread(target=s.startServer).start()

    while 1:       
        #s._broadcast()
        if(len(s.player_names) >= 2): #at least two players and we will start
            if(state == 0):#game in progress
                SM_NEW_GAME = { 'num_players' : len(s.CLIENTS),
                                'player_names' : s.player_names,
                                'num categories' : s.num_categories,
                                'categories' : s.categories,
                                'ques_in_categories' : s.ques_in_categories,
                                'def_timeout' : s.def_timeout }          
                s.broadcast(SM_NEW_GAME)
                state = 1
            elif(state == 1):#round in progress
                selected_player = random.randint(1,len(s.CLIENTS)+1)
                if(selected_player >= len(s.CLIENTS)):
                    selected_player = selected_player -1
                SM_NEW_ROUND = {"selected_player" : selected_player}
                s.broadcast(SM_NEW_ROUND)
                #test = input("Waiting for category here...")
                state = 2
            elif(state == 2):#category selected
                if(s.SM_CATEGORY["category"] > -1): #category index begins from 0
                    s.broadcast(s.SM_CATEGORY)
                    state = 3
            elif(state == 3):#display question
                selected_question = random.randint(0,2) #question indexes are 0 or 1
                if(selected_question >= 2):
                    selected_question = selected_question -1
                SM_QUESTION = {"question" : s.questions[s.SM_CATEGORY['category']][selected_question]}
                s.broadcast(SM_QUESTION)
                start_time = time.time()             
                state = 4
            elif(state == 4): #wait for ring
                if(s.SM_RING_CLIENT["player_id"] == 100):
                    s.broadcast(s.SM_RING_CLIENT)
                    correct_answer = s.answers[s.SM_CATEGORY["category"]][selected_question]
                    s.SM_ANSWER["correct_answer"] = correct_answer
                    state = 5 #wait for answer
                elif(s.SM_RING_CLIENT["player_id"] > 0):
                    s.broadcast(s.SM_RING_CLIENT)
                    state = 5 #wait for answer                
            elif(state == 5): #wait for answer
                if(s.SM_ANSWER["correct_answer"] != ""):
                    s.broadcast(s.SM_ANSWER)
                    state = 6 #end of round
            elif(state == 6): #end of round
                end_round = {"end" : "END OF ROUND"}
                s.broadcast(end_round)
                state = 7
        pprint.pprint(s.CLIENTS)
        print(len(s.CLIENTS)) #print out the number of connected clients every 3s        
        time.sleep(1)
