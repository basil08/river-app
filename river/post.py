import functools 

from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.security import check_password_hash, generate_password_hash

from river.db import get_db
from river.auth import login_required

bp = Blueprint('post', __name__, url_prefix='/p')

@bp.route('/<int:post_id>')
def index(post_id):
  db = get_db()
  post = db.execute('SELECT * FROM post WHERE post_id = ?', (post_id,)).fetchone()
  comments = db.execute('SELECT * FROM comment WHERE post_id = ?', (post_id,)).fetchall()
  return render_template('post/index.html', post=post, comments=comments)




@bp.route('/new', methods = ['GET', 'POST'])
def new():
  if request.method == 'POST':
    db = get_db()
    error = None
    title = request.form['title']
    body = request.form['body']

    # verify data
    if not title:
      error = 'Title is required'
    elif not body:
      error = 'Body cannot be empty.'
    elif len(body) < 3:
      error = 'Body must have atleast 3 characters'
    
    if error is None:
      # insert into db 
      db.execute('INSERT INTO post (author_id, title, body) VALUES (?,?,?);', (g.user['user_id'], title, body))
      # get the id of the post just inserted, used to redirect to the post's index page 
      post = db.execute('SELECT * FROM post WHERE author_id = ? AND title = ?', (g.user['user_id'], title)).fetchone()
      db.commit()

      # and redirect
      return redirect(url_for('post.index', post_id=post['post_id']))
    
    flash(error)
  return render_template('post/new.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:post_id>/edit')
@login_required
def edit(post_id):
  pass
  return render_template('post/edit.html')