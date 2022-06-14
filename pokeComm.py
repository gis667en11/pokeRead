import jsonpickle
import functionsTiming as funTime

# Echo server program
import socket
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
SEND_PERIOD = 100


class Button:
    def __init__(self):
        self.count = 0
        self.prevCount = 0
        self.pulse_Pressed = False

class CommHandler:
    def __init__(self):
        self.periodTimer = funTime.TimerON()
        self.sock = 0
        self.client = 0
        self.addr = 0
        self.imageCaptureCount = 0
        self.hashFlat = False
        self.hashMatch = False
        self.tbDialogue = False
        self.tbGrey = False
        self.tbFight = False
        self.recordState = 0

commHandler = CommHandler()
buttons = []

class sendData:
    def __init__(self):
        self.slider = []
        self.button = []

def init_socketServer() :
    global commHandler
    global buttons

    buttons = [Button() for i in range(10)]
    commHandler.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    commHandler.sock.bind((HOST, PORT))
    commHandler.sock.listen(1)
    commHandler.sock.setblocking(False)
    commHandler.client = None

def handle_socketServer() :
    global commHandler
    global buttons

    # Initialize pulse bits
    for b in buttons:
        b.pulse_Pressed = False
    
    # Attempt to allow connection with client
    if commHandler.client is None:
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

            commHandler.periodTimer.reset()            

            msgPayload = {}
            msgPayload['dataReq'] = True
            msgPayload['captureCount'] = commHandler.imageCaptureCount
            msgPayload['flatHash'] = commHandler.hashFlat
            msgPayload['tbBlue'] = commHandler.tbDialogue
            msgPayload['tbGrey'] = commHandler.tbGrey
            msgPayload['tbFight'] = commHandler.tbFight
            msgPayload['recordState'] = commHandler.recordState
            jsonDumpStr = jsonpickle.dumps(msgPayload)
            jsonDumpBytes = jsonDumpStr.encode('UTF-8')

            try:
                commHandler.client.sendall(jsonDumpBytes)
            except:
                commHandler.client = None

        try:
            raw = commHandler.client.recv(1024)
        except:
            pass
        else:
            if raw:
                rawString = raw.decode('utf-8')
                panelData = jsonpickle.decode(rawString)
                buttonsDict = panelData.get('buttons')
                if buttonsDict:
                    index0 = 0
                    for b in buttonsDict:
                        if index0 < len(buttons):
                            buttons[index0].count = list(b.values())[0]
                            if buttons[index0].count != buttons[index0].prevCount:
                                buttons[index0].pulse_Pressed = True
                                buttons[index0].prevCount = buttons[index0].count
                                print(f'Button {index0} pressed!')
                            index0 = index0 + 1


if __name__ == "__main__":

    init_socketServer()

    incrementCountTimer = funTime.TimerON()
    incrementCountTimer.preset = 2000

    while True:
        
        if incrementCountTimer.run(1):
            incrementCountTimer.reset()
            commHandler.imageCaptureCount += 1

        handle_socketServer()
        

