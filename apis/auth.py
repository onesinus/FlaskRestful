import functools

from flask import (
    Blueprint, g, session, request
)

from werkzeug.security import check_password_hash, generate_password_hash

from apis.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES(?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return ({ 'success': True, 'data': { 'username': username } })
        return ({ 'success': False, 'error': error }, 400)

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        
        if error is None:
            session.clear()
            session['user_id'] = user[0]

            return {
                'success': True,
                'data': {
                    'user_id': user[0],
                    'username': user[1]
                }
            }

        return {
            'success': False,
            'error': error
        }

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    
    g.user = get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    g.user = None
    return {
        "success": True
    }

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return ({
                'success': False,
                "error": "You are not authorized to access this endpoint"
            },401)

        return view(**kwargs)            
        
    return wrapped_view