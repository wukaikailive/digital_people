import socketio
import eventlet

sio = socketio.Server(async_mode='eventlet', ping_timeout=3600)
app = socketio.Middleware(sio)


@sio.event
def connect(sid, environ):
    print('connect', sid)


@sio.event
def cmd(sid, msg):
    sio.emit(msg['name'], msg['text'])


@sio.event
def cancel_idle_timer(sid, msg):
    sio.emit('cancel_idle_timer')


@sio.event
def re_start_idle_timer(sid, msg):
    sio.emit('re_start_idle_timer')


@sio.event
def receive_user_barrage(sid, msg):
    sio.emit('receive_user_barrage', msg)


@sio.event
def disconnect(sid):
    print('disconnect', sid)


def socket_server_start():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8082)), app)


if __name__ == '__main__':
    socket_server_start()
