from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .auth import jwt_token_required
from flaskr.db import get_db
from pymongo import MongoClient
import jwt
from datetime import datetime, date
import hashlib


bp = Blueprint('blog', __name__)

client = MongoClient('localhost',27017)
db = client.dbLFD

SECRET_KEY = 'apple'

@bp.route('/blog')
def index():
    posts = db.user_test4.find()    
    return render_template('blog/index.html', posts=posts)

@bp.route('/blog/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title_receive = request.form['blog_title_give']
        body_receive = request.form['blog_body_give']
        tag_receive = request.form['blog_tag_give']
        token_receive = request.headers['token_give']
        created_time = datetime.now()
        error = None        
        if title_receive is None:
            error = 'title is required'
            return jsonify({'result':'fail', 'msg':error})
        elif body_receive is None:
            error = 'body is required'
            return jsonify({'result':'fail', 'msg':error})
        elif token_receive is not None:        
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])            
            userinfo = db.user_test3.find_one({'email':payload['email']},{'_id':0})                     
            username = userinfo['username']
            print(title_receive, body_receive, tag_receive, token_receive, created_time)
            print(userinfo)
            db.blog_test2.insert_one({'title':title_receive, 'body':body_receive, 'author':username, 'created_time':created_time, 'tag':tag_receive})
            return jsonify({'result':'success', 'msg':'포스팅이 완료되었습니다.'})
        else:                                    
            return jsonify({'result':'fail', 'msg':'something wrong'})
    return render_template('blog/create.html')

@bp.route('/blog/get_posting', methods=('GET', 'POST'))
def get_posting():    
    posted_blog = list(db.blog_test2.find({},{'_id':0}))
    print(posted_blog)
    return jsonify({'result':'success', 'articles':posted_blog})        

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@jwt_token_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@jwt_token_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/blog/post/[회계장부열람등사가처분 - 01] 대표이사의 횡령배임에 대한 대응으로 주주나 사원의 회계장부열람등사가처분의 필요성')
def blog_post_1():    
    return render_template('blog/post/post_01.html')

@bp.route('/blog/post')
def blog_post():    
    posted_blog = list(db.blog_test2.find({},{'_id':0}))        
    print(posted_blog)
    print(posted_blog[0]['title'])
    return render_template('blog/post/post_base.html')