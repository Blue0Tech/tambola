import socket
from threading import Thread
import time
import random

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 5000
CLIENTS = {}

flashNumberList = [i for i in range(0,30)]

gameOver = False
playersJoined = False

def handleClient():
    global CLIENTS
    global flashNumberList
    global gameOver
    global playersJoined

    while(True):
        if(gameOver):
            break
        try:
            if(len(list(CLIENTS.keys())) >= 2 and not gameOver):
                if(not playersJoined):
                    playersJoined = True
                    time.sleep(1)
                if(len(flashNumberList) > 0):
                    randomNumber = random.choice(flashNumberList)
                    currentName = None
                    try:
                        for cname in CLIENTS:
                            currentName = cname
                            csocket = CLIENTS[cname]['player_socket']
                            csocket.send(str(randomNumber).encode('utf-8'))
                        flashNumberList.remove(int(randomNumber))
                    except:
                        del CLIENTS[currentName]
                    time.sleep(3)
                else:
                    gameOver = True
        except:
            gameOver = True

def receiveMessage(player_socket):
    global CLIENTS
    global gameOver
    print('in receive msgs function')
    while(True):
        try:
            message = player_socket.recv(2048).decode('utf-8')
            print(message)
            if(message):
                for cname in CLIENTS:
                    csocket = CLIENTS[cname]['player_socket']
                    if('wins the game.' in message):
                        print('game won')
                        gameOver = True
                    csocket.send(message.encode('utf-8'))
        except:
            pass

def setup():
    print('\n\t\t\t\t\t\t\t*** Welcome to Tambola game ***\n')
    
    global SERVER
    global IP_ADDRESS
    global PORT

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)

    print('\t\t\t\t\t\t*** Server is waiting for incoming connections ***\n')
    thread = Thread(target=handleClient,args=())
    thread.start()
    acceptConnections()

def acceptConnections():
    global CLIENTS
    global SERVER

    while (True):
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode('utf-8').strip()
        print(player_name)
        if(len(CLIENTS.keys())==0):
            CLIENTS[player_name] = {'player_type':'player1'}
        else:
            CLIENTS[player_name] = {'player_type':'player2'}
        CLIENTS[player_name] = {
            'player_socket':player_socket,
            'address':addr,
            'player_name':player_name
        }

        print(f'Connection established with {player_name} : {addr}')
        
        thread1 = Thread(target = receiveMessage,args=(player_socket,))
        thread1.start()

setup()