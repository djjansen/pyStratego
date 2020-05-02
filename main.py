from flask import Flask, render_template, request, flash, session, g, Blueprint
from flask_socketio import SocketIO, join_room, leave_room
from bson.objectid import ObjectId
import auth
import db
from auth import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
app.register_blueprint(auth.bp)
active_rooms=[]


@app.route('/')
@login_required
def main():
	redirect(url_for('sessions',id=session.get('session_id')))

@app.route('/session/<string:id>', methods=("GET","POST"))
@login_required
def sessions(id):
	room = session.get('session_id')
	messages = db.fetchOne({'_id': ObjectId(room)})['messages']
	g.messages = [message for message in messages if len(message) == 2]
	print('...................')
	print(g.messages)
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
    if room in active_rooms:
        # add player and rebroadcast game object
        # rooms[room].add_player(username)
        join_room(room)
        send(active_rooms[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    room = session.get('session_id')
    socketio.emit('my response', json, callback=messageReceived,room=room)
    gameSession = db.fetchOne({'_id': ObjectId(room)})
    print(gameSession)
    gameSession['messages'].append(json)
    db.updateOne({'_id': ObjectId(room)},{'$set':{'messages':gameSession['messages']}})


if __name__ == '__main__':
    socketio.run(app, debug=True)