import functools
import db
import random
import string
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, g
    )
from werkzeug.security import check_password_hash, generate_password_hash

#Board class with one object, initializes in prep mode with empty grid
class board:
    def __init__(self):
        self.status = 'preparation'
        self.grid = {chr(alpha):{str(num+1):{'color':'none','piece':""} for num in range(10)} for alpha in range(ord("A"),ord("K"))}
        
    def updateGrid(self,origin,destination):
        
        def replaceValue(inputVar,newValue):
            self.grid[inputVar["X"]][inputVar["Y"]] = newValue
            
        replaceValue(origin,"")
        replaceValue(destination,"%")

#create board object
board = board()


#Used to generate game codes
def get_random_alphaNumeric_string(stringLength=5):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))



bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/login', methods=('GET', 'POST'))
def enterGame():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        session_code = None

        try:
            session_code = request.form['session_code']
            print('session found: ' + session_code)
        except:
            print('no code found')
        if session_code is None:
            session_code = get_random_alphaNumeric_string(5)
            db.createSession({'code':session_code,
                            'users':[],
                            'board_state':board.grid,
                            'messages':[]})
            print('session created: ' + session_code)
            print(board.grid)

        if username is None:
            error = 'Please provide a username. You can make one up.'

        else:
            gameSession = db.fetchOne({'code':session_code})
            session.clear()
            if username in gameSession['users']:
                if not check_password_hash(users[username]['password'], password):
                    error = 'Incorrect password.'
            else:
                if len(gameSession['users']) == 1:
                    color = 'red'
                else:
                    color = 'blue'
                gameSession['users'].append({username:{'password':generate_password_hash(password),'color':color}})
                db.updateOne({'code':session_code},{'$set':{'users':gameSession['users']}})

        session_id = str(gameSession['_id'])

        if error is None:
            session['user_id'] = username
            session['session_code'] = session_code
            session['session_id'] = session_id
            session['color'] = str(color)
            return redirect( url_for('sessions', id=session_id))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.enterGame'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    session_id = session.get('session_id')
    session_code = session.get('session_code')

    if user_id is None:
        g.user = None
    else:
        print('getting user info')
        g.user = user_id
        g.session_id = session_id
        g.session_code = session_code

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.enterGame'))
        print('user found')
        print(g.user)
        return view(**kwargs)
    print('returning view')
    return wrapped_view

