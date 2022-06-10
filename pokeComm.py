import json
import functionsTiming
import jsonpickle
import functionsTiming as funTime

# Echo server program
import socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
SEND_PERIOD = 250

class CommHandler:
    def __init__(self):
        self.periodTimer = funTime.TimerON()
        self.sock = 0
        self.client = 0
        self.addr = 0

commHandler = CommHandler()

class sendData:
    def __init__(self):
        self.slider = []
        self.button = []

def init_socketServer() :
    global commHandler
    commHandler.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    commHandler.sock.bind((HOST, PORT))
    commHandler.sock.listen(1)
    commHandler.sock.setblocking(False)
    commHandler.client = None

def handle_socketServer() :
    global commHandler

    # Attempt to allow connection with client
    if commHandler.client is None:
        sent = 0
        try:
            commHandler.client, commHandler.addr = commHandler.sock.accept()
        except BlockingIOError:
            commHandler.client = None
        else:
            print('Connected by', commHandler.addr)
    
    # This executes if a client is connected
    else:
        # Send data once ever send period
        commHandler.periodTimer.run(1,SEND_PERIOD)
        

        if commHandler.periodTimer.done:

            print("attempting send...")
            commHandler.periodTimer.reset()            

            msgString = "received" 
            try:
                commHandler.client.sendall(msgString.encode('ascii'))
            except BlockingIOError:
                commHandler.client = None
            except ConnectionAbortedError:
                commHandler.client = None
        
        try:
            raw = commHandler.client.recv(1024)
        except:
            pass
        else:
            if raw:
                rawString = raw.decode('utf-8')
                # print(rawString)

if __name__ == "__main__":

    init_socketServer()

    while True:

        handle_socketServer()
        

