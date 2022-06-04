import socketio
import time
# install requests, websocket-client

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

if __name__ == '__main__':

    sio.connect('http://localhost:5000')

    currentMillis = int( time.time() * 1000 ) # time() is epoch in seconds
    prevMillis = currentMillis

    while True:

        currentMillis = int( time.time() * 1000 ) # time() is epoch in seconds

        if (currentMillis - prevMillis > 1000):
            print('tick')
            sio.emit('tick', currentMillis)
            prevMillis = currentMillis