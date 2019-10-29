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
