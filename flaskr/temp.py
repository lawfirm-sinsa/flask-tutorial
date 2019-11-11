@bp.route('/blog/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title_receive = request.form['blog_title_give']
        body_receive = request.form['blog_body_give']
        token_receive = request.headers['token_give']
        error = None
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])            
            userinfo = db.user_test3.find_one({'email':payload['email']},{'_id':0})                     
            username = userinfo['username']
            return jsonify({'result':'success', 'username':username})   
        except jwt.ExpiredSignatureError:
            return jsonify({'result':'fail', 'msg':'로그인 시간이 만료되었습니다'})
        if not title_receive:
            error = 'Title is required.'
        elif not body_receive:
            error = 'body is required.'        
        else:            
            db.blog_test1.insert_one({'title':title_receive, 'body':body_receive, 'author':username})
            bloginfo = db.blog_test1.find_one({'title':title_receive})
            print(bloginfo)
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
post = db.blog_test1.find({'_id':g.user['id']})
"""post = get_db().execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
).fetchone()"""
if post is None:
    abort(404, "Post id {0} doesn't exist.".format(id))

if check_author and post['author_id'] != g.user['id']:
    abort(403)
return post

# auth.py backup / 2019. 11. 09. 

import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

client = MongoClient('localhost',27017)
db = client.dbLFD

SECRET_KEY = 'apple'

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username_give']
        email = request.form['email_give']
        password = request.form['password_give']

        pw_hash = generate_password_hash(password)
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
        if error is None:
            db.user_test3.insert_one({'username':username, 'email':email, 'password':pw_hash})                
            #db.user_test3.insert_one({'username':username, 'email':email, 'password':generate_password_hash(password)})                
            return jsonify({'result':'success'})
        else:
            return jsonify({'result':'fail'})
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email_give']
        password = request.form['password_give']        
        error = None
        user = db.user_test3.find_one({'email':email})            
        print(user)
        if user is None:            
            return jsonify({'result':'fail', 'msg':'email is incorrect'})
        elif not check_password_hash(user['password'], password):
            return jsonify({'result':'fail', 'msg':'password is incorrect'})        
        else:            
            payload = {
                'email' : email,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            print(token)
            return jsonify({'result':'success', 'msg':'로그인 성공', 'token':token})        
    return render_template('auth/login.html')

@bp.route('/validation', methods=['GET'])
def api_valid():
    token_receive = request.headers['token_give']
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        userinfo = db.user_test3.find_one({'email':payload['email']},{'_id':0})         
        print(userinfo)
        return jsonify({'result':'success', 'userinfo':userinfo, 'username':userinfo['username']})   
    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail', 'msg':'로그인 시간이 만료되었습니다'})

def jwt_token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not 'token_give' in request.headers:
            return jsonify({
                'msg':'token is not given'
            }), 400
        token_receive = request.headers['token_give']
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        except:
            return jsonify({
                'msg' : 'invalid token given'
            }), 400
        kwargs['payload'] = payload
        return func(*args, **kwargs)        
    return decorated_function


@bp.route('/logout')
def logout():
    token = ""
    return redirect(url_for('index.home'))


