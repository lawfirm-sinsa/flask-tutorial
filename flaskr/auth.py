import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from pymongo import MongoClient

bp = Blueprint('auth', __name__, url_prefix='/auth')

client = MongoClient('localhost',27017)
db = client.dbLFD

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username_give']
        email = request.form['email_give']
        password = request.form['password_give']
        #db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.user_test3.find_one({'username':request.form['username_give']}):
            error = 'User {} is already registered.'.format(username)
        elif db.user_test3.find_one({'email':request.form['email_give']}):
            error = 'email {} is already registered.'.format(email)
        """elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)"""
        """if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()"""
        if error is None:
            db.user_test3.insert_one({'username':username, 'email':email, 'password':generate_password_hash(password)})                
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email_give']
        password = request.form['password_give']
        #db = get_db()
        error = None
        user = db.user_test3.find_one({'email':request.form['email_give']})            
        print(user)
        if user is None:
            error = 'Incorrect email.'            
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'            
        if error is None:
            session.clear()
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index.home'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = str(db.user_test3.find_one({'_id':user_id}))
        #g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view