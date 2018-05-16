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

class server():

    def __init__(self):
        self.CLIENTS = []
        self.player_names = []
        self.num_categories = 5
        self.categories = ['Movies','Sportsmen','Capital Cities','US History','Artists']
        self.ques_in_categories = 2
        self.questions = [['Best Oscar Movie 2017','Highest Grossing Movie of all time'],
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
        self.def_timeout = 5000
        self.SM_CATEGORY = {'category' : 0}


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
                elif('category' in client_message.keys()):#select category
                    print("Category ", client_message["category"])
                    self.SM_CATEGORY['category'] = client_message["category"]                    

         # the connection is closed: unregister
        #sself.CLIENTS.remove(client_socket)
        #client_socket.close() #do we close the socket when the program ends? or for ea client thead?

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
        sock.send(bytes('{"type": "bet","value": "1"}', 'UTF-8'))


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
            elif(state == 2):
                if(s.SM_CATEGORY["category"] > 0):
                    s.broadcast(s.SM_CATEGORY)
                    state = 3
        pprint.pprint(s.CLIENTS)
        print(len(s.CLIENTS)) #print out the number of connected clients every 5s        
        time.sleep(3)
