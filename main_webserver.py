import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def tick(sid, data):
    print('tick', data)
    sio.emit('tock', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# import eventlet
# import socketio
# import asyncio
# import time

# # sio = socketio.Server()
# # app = socketio.ASGIApp(sio, static_files={
# #     '/': {'content_type': 'text/html', 'filename': 'index.html'}
# # })

# from aiohttp import web
# import socketio

# sio = socketio.AsyncServer()
# app = web.Application()
# sio.attach(app)

# async def index(request):
#     """Serve the client-side application."""
#     with open('index.html') as f:
#         return web.Response(text=f.read(), content_type='text/html')

# @sio.event
# def connect(sid, environ):
#     print("connect ", sid)

# @sio.event
# async def chat_message(sid, data):
#     print("message ", data)

# @sio.event
# def disconnect(sid):
#     print('disconnect ', sid)

# # app.router.add_static('/static', 'static')
# # app.router.add_get('/', index)

# # async def main():
# #     web.run_app(app)

# # if __name__ == '__main__':
# #     asyncio.run(main())
# #     print("bruh")

# #     # asyncio.run(main())


# # currentMillis = 0
# # prevMillis = 0

# async def main():
#     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

# #     # currentMillis = int( time.time() * 1000 ) # time() is epoch in seconds
# #     # prevMillis = currentMillis

# #     # while True:

# #     #     currentMillis = int( time.time() * 1000 ) # time() is epoch in seconds

# #     #     if (currentMillis - prevMillis > 1000):
# #     #         sio.emit('tick', currentMillis)
# #     #         prevMillis = currentMillis
        
        
# #     print('test!!!')
    
# #     print('lowlz')

# if __name__ == '__main__':
#     asyncio.run(main())
