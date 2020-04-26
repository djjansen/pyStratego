from flask import Flask, render_template, request, flash, session, g, Blueprint
from flask_socketio import SocketIO, join_room, leave_room
import auth
from auth import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
app.register_blueprint(auth.bp)
active_rooms=[]


@app.route('/')
@login_required
def main():
	return render_template('session.html')

@app.route('/session/<string:id>', methods=("GET","POST"))
@login_required
def sessions(id):
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('create')
def create_room(data):
    """Create a game lobby"""
    room = data['data']
    print(room)
    active_rooms.append(room)
    print(join_room(room))
    socketio.emit('join_room', {'room': room})

@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    room = data['room']
    if room in ROOMS:
        # add player and rebroadcast game object
        # rooms[room].add_player(username)
        join_room(room)
        send(ROOMS[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    room = session.get('session_id')
    socketio.emit('my response', json, callback=messageReceived,room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)