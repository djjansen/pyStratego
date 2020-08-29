from flask import Flask, render_template, request, redirect,url_for, flash, session, g, Blueprint
from engineio.payload import Payload
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
	sessionObject = db.fetchOne({'_id': ObjectId(room)})
	messages = sessionObject['messages']
	session['unplaced_pieces'] = sessionObject['unplaced_pieces'][session['user_id']]
	session['board_state'] = g.board_state = sessionObject['board_state']
	session['phase'] = sessionObject['phase']
	g.messages = [message for message in messages if len(message) == 2]
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
        socketio.send(active_rooms[room].to_json(), room=room)
    else:
        socketio.emit('error', {'error': 'Unable to join room. Room does not exist.'})

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
def handle_board_state_change(json, methods=['GET', 'POST']):
	print('received board state: ' + str(json))
	username = session['user_id']
	room = session.get('session_id')
	board_state = session.get('board_state')
	board_state = {row:{key:{'color':value['color'],'piece':value['piece']} for key, value in sorted(board_state[row].items(), key=lambda item: int(item[0]))} for row in board_state}
	origin_row = json['origin_cell'][0]
	origin_col = json['origin_cell'][1]
	destination_row = json['destination_cell'][0]
	destination_col = json['destination_cell'][1]

	unplaced_pieces = session.get('unplaced_pieces')
	if json['origin_cell'] != ['','']:
		board_state[origin_row][origin_col]['piece'] = ""
		board_state[origin_row][origin_col]['color'] = "none"
	else:
		for piece in unplaced_pieces:
			if piece[0] == json['moved_piece']['piece']:
				piece[1] -= 1

	#if two pieces from different teams collide, do battle

	def combat(piece1,piece2):
		if piece2['piece'] == '#':
			result = 'victory'
		elif auth.pieces_reference[piece1['piece']].weakness == piece2['piece']:
			result = piece2
		elif auth.pieces_reference[piece2['piece']].weakness == piece1['piece']:
			result = piece1
		elif auth.pieces_reference[piece1['piece']].rank < auth.pieces_reference[piece2['piece']].rank:
			result = piece1
		elif auth.pieces_reference[piece1['piece']].rank == auth.pieces_reference[piece2['piece']].rank:
			result = {'piece':"",'color':'none'}
		elif auth.pieces_reference[piece1['piece']].rank > auth.pieces_reference[piece2['piece']].rank:
			result = piece2

		return result

	if board_state[destination_row][destination_col]['color'] not in ['none',json['moved_piece']['color']]:
		new_piece = combat(json['moved_piece'],board_state[destination_row][destination_col])
		if new_piece == 'victory':
			print('yay!')
		json['moved_piece'] = new_piece
		print(json)
		socketio.emit('own combat result', json, room=room)
		
	else:
		new_piece = json['moved_piece']

	board_state[destination_row][destination_col] = new_piece
	
	# fetch room info from db
	gameSession = db.fetchOne({'_id': ObjectId(room)})
	# update unplaced pieces record
	gameSession['unplaced_pieces'][username] = unplaced_pieces
	current_phase = gameSession['phase']

	# sum up total pieces unplaced, change phases if necessary
	total_pieces = 0
	if current_phase == "preparation":
		for user in gameSession['unplaced_pieces']:
			for piece in gameSession['unplaced_pieces'][user]:
				print(piece)
				total_pieces += piece[1]
	
		print(total_pieces)

		if total_pieces == 0:
			current_phase = "blue"
			print('condition met....')

	elif current_phase == "blue":
		current_phase = "red"
	
	elif current_phase == "red":
		current_phase = "blue"

	json['phase'] = current_phase
	# emit response to clients 
	socketio.emit('my response', json, callback=messageReceived,room=room)

	# update unplaced pieces record for this player, to be re-inserted in db below
	gameSession['unplaced_pieces'][username] = unplaced_pieces
	# update board state, phase, and unplaced pieces records in database
	db.updateOne({'_id': ObjectId(room)},
					{'$set':{'board_state':board_state,
					'unplaced_pieces':gameSession['unplaced_pieces'],'phase':current_phase}})
	# update same attributes from above in user's session cookie
	session['board_state'], session['unplaced_pieces'], session['phase'] = board_state, unplaced_pieces, current_phase


@socketio.on('opposing board sync')
def sync_opposing_move(methods=['GET', 'POST']):
	room = session.get('session_id')
	gameSession = db.fetchOne({'_id': ObjectId(room)})
	session['board_state'], session['phase'] = [gameSession[attribute] 
												for attribute in ['board_state','phase']]


@socketio.on('get range')
def return_range(json, methods=['GET', 'POST']):
	room, board_state  = (session.get(attribute) for attribute in ('session_id', 'board_state'))

	selectedRow, selectedCol = json['coordinates'][0], json['coordinates'][1]
	own_team = json['color']
	print(json)
	print(board_state)
	selectedPiece = board_state[selectedRow][selectedCol]['piece']
	moveRange = auth.pieces_reference[selectedPiece].movementRange

	viableSquares = {}

	def addViableSquare(row,col):
		if row in viableSquares:
			if col not in viableSquares[row]:
				viableSquares[row].append(col)
		else:
			viableSquares[row] = [col]

	greaterBlockingRows = {'blocking':[11],'opposing':[10]}
	lesserBlockingRows = {'blocking':[0],'opposing':[1]}
	greaterBlockingCols = {'blocking':[11],'opposing':[10]}
	lesserBlockingCols = {'blocking':[0],'opposing':[1]}

	# check if square should block movement of another piece, modify the dicts above to help return viable moves
	def check_if_block(square, dict, item, team=own_team):
		if square['color'] not in ['water',own_team]:
			dict['opposing'].append(item)
		else:
			dict['blocking'].append(item)

	# iterate through rows and populate blocking dictionaries
	for row in board_state:
		# starting with rows
		row_diff = ord(selectedRow) - ord(row)
		if  abs(row_diff) <= moveRange and abs(row_diff) > 0:
			row_index = ord(row) - 64
			if board_state[row][selectedCol]['color'] != "none":
				if row_diff > 0:
					check_if_block(square=board_state[row][selectedCol], dict=lesserBlockingRows, item=row_index)
				elif row_diff < 0:
					check_if_block(square=board_state[row][selectedCol], dict=greaterBlockingRows, item=row_index)

		# then with columns
		if row_diff == 0:
			for num in range(int(selectedCol) - moveRange, int(selectedCol) + moveRange + 1):
				if num in range(1,11):
					if board_state[row][str(num)]['color'] != 'none':
						if num > int(selectedCol):
							check_if_block(square=board_state[row][str(num)], dict=greaterBlockingCols, item=num)
						elif num < int(selectedCol):
							check_if_block(square=board_state[row][str(num)], dict=lesserBlockingCols, item=num)

			# sort the lists 		
			greaterBlockingCols['opposing'].sort()
			lesserBlockingCols['opposing'].sort(reverse=True)

			# re-iterate through columns to add viable squares
			for num in range(int(selectedCol) - moveRange, int(selectedCol) + moveRange + 1):
				if num in range(1,11):
					if board_state[row][str(num)]['color'] not in [own_team,'water']:
						if (num > max(lesserBlockingCols['blocking']) and (num < min(greaterBlockingCols['blocking']))):
							if (num >= lesserBlockingCols['opposing'][0]) and (num <= greaterBlockingCols['opposing'][0]):
								addViableSquare(ord(row) - 64,num)

		# sort the row lists
		greaterBlockingRows['opposing'].sort()
		lesserBlockingRows['opposing'].sort(reverse=True)

	# re-iterate through rows to add viable squares
	for row in board_state:
		row_diff = ord(selectedRow) - ord(row)
		if  abs(row_diff) <= moveRange and abs(row_diff) > 0:
			row_index = ord(row) - 64

			if board_state[row][selectedCol]['color'] not in ['water', own_team]:
				if (row_index > max(lesserBlockingRows['blocking'])) and row_index < min(greaterBlockingRows['blocking']):
					if (row_index >= lesserBlockingRows['opposing'][0]) and (row_index <= greaterBlockingRows['opposing'][0]):
						addViableSquare(row_index,int(selectedCol))

	# send final viable quares to client
	socketio.emit('return range', viableSquares, room=room)


#when this file is run, start flask-socketio app
if __name__ == '__main__':
    socketio.run(app, debug=True)