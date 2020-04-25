from flask import Flask, render_template, request, flash, session, g, Blueprint
from flask_socketio import SocketIO
import auth
from auth import login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
app.register_blueprint(auth.bp)

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

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)