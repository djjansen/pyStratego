from flask import Flask, render_template, request, redirect,url_for, flash, session, g, Blueprint
from flask_socketio import SocketIO, join_room, leave_room
from bson.objectid import ObjectId
import auth
import db
from auth import login_required

#app definition and config, see bottom of file for
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
app.register_blueprint(auth.bp)
active_rooms=[]

#create list of piece objects and quanitities needed
class piece:
    def __init__(self,rank,weakness,movementRange,maxQuantity):
        self.weakness = weakness
        self.rank = rank
        self.movementRange = movementRange
        self.maxQuantity = maxQuantity
        
pieces_reference = {"B":piece(0,"8",0,6),
					"1":piece(1,"",1,1),
                    "2":piece(2,"",1,1),
                    "3":piece(3,"",1,2),
                    "4":piece(4,"",1,3),
                    "5":piece(5,"",1,4),
                    "6":piece(6,"",1,4),
                    "7":piece(7,"",1,4),
                    "8":piece(8,"B",1,5),
                    "9":piece(9,"",9,8),
                    "S":piece(10,"",1,1),
                    "#":piece(11,"",0,1)}

#main route, redirects to appropriate session page if logged in
@app.route('/')
@login_required
def main():
	return redirect(url_for('sessions',id=session.get('session_id')))

#session page route, adds session id to endpoint
#1. fetches session document from db, saves messages to g
#2. saves board state to session
#3. returns session page
@app.route('/session/<string:id>', methods=("GET","POST"))
@login_required
def sessions(id):
	room = session.get('session_id')
	messages = db.fetchOne({'_id': ObjectId(room)})['messages']
	session['pieces_reference'] = [(key,pieces_reference[key].maxQuantity) for key in pieces_reference]
	session['board_state'] = db.fetchOne({'_id': ObjectId(room)})['board_state']
	g.messages = [message for message in messages if len(message) == 2]
	g.board_state = db.fetchOne({'_id': ObjectId(room)})['board_state']
	print(g.board_state)
	return render_template('session.html')

#callback function used in socket emits later
def messageReceived(methods=['GET', 'POST']):
	print('message was received')

#listener for room creation
#1. get room id from socket emit
#2. join empty room (creating it)
#3. emit joined room message
@socketio.on('create')
def create_room(data):
    room = data['data']
    active_rooms.append(room)
    join_room(room)
    socketio.emit('join_room', {'room': room})

#listener for room joining
#1. get room id from socket emit
#2. check if room exists, send error message if not
#3. if exists, join room and send message
@socketio.on('join')
def on_join(data):
    room = data['room']
    if room in active_rooms:
        join_room(room)
        send(active_rooms[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

#listener for chat messages
#1. get room from session id
#2. emit message on 'my response' channel, which listener on session.html adds message to page
#3. get session document db, add new message, update in db
@socketio.on('chat message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    room = session.get('session_id')
    socketio.emit('my response', json, callback=messageReceived,room=room)
    gameSession = db.fetchOne({'_id': ObjectId(room)})
    gameSession['messages'].append(json)
    db.updateOne({'_id': ObjectId(room)},{'$set':{'messages':gameSession['messages']}})

#listener for board states
#1. get room from session id
#2. send board state...incomplete
@socketio.on('board state')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	print('received board state: ' + str(json))
	room = session.get('session_id')
	board_state = session.get('board_state')
	board_state = {row:{key:{'color':value['color'],'piece':value['piece']} for key, value in sorted(board_state[row].items(), key=lambda item: int(item[0]))} for row in board_state}
	origin_row = json['origin_cell'][0]
	origin_col = json['origin_cell'][1]
	destination_row = json['destination_cell'][0]
	destination_col = json['destination_cell'][1]
	if json['origin_cell'] != ['','']:
		board_state[origin_row][origin_col] = ""
	print(json)
	board_state[destination_row][destination_col]['piece'] = json['moved_piece']['piece']
	board_state[destination_row][destination_col]['color'] = json['moved_piece']['team']
	print(board_state)
	socketio.emit('my response', json, callback=messageReceived,room=room)
	gameSession = db.fetchOne({'_id': ObjectId(room)})
	db.updateOne({'_id': ObjectId(room)},{'$set':{'board_state':board_state}})
	session['board_state'] = board_state

#when this file is run, start flask-socketio app
if __name__ == '__main__':
    socketio.run(app, debug=True)