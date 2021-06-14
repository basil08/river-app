import functools 

from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)

from werkzeug.security import check_password_hash, generate_password_hash

from river.db import get_db
from river.auth import login_required

bp = Blueprint('user', __name__, url_prefix='/u')

@bp.route('/home')
@login_required
def home():
  # show a list of random posts for now...
  # TODO: allow non-logged in users to access /home and show list of random posts
  # But if logged in users, show posts from relevant sources, followers etc
  error = None
  db = get_db()
  pagination_limit = 15

# SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' ORDER BY created DESC'
    # SELECT p.post_id, title, body, created, author_id, username FROM post p JOIN user_detail u 
      # ON p.author_id = u.user_id LIMIT 15 ORDER BY created DESC'''
  query = 'SELECT post_id, title, body, created, author_id, username FROM post JOIN user_detail ON post.author_id = user_detail.user_id ORDER BY created DESC;'
  posts = db.execute(query).fetchall()

  return render_template("social/home.html", posts=posts)


@bp.route('/<string:username>')
def profile(username):
  error = None
  db = get_db()
  user = db.execute(' \
  SELECT * FROM user_detail WHERE username = ?', (username,)
  ).fetchone()

  if not user:
    error = 'Error. User @{} does not exist.'.format(username)
    flash(error)

  # template checks if error is not None
  # accordingly, fills the table
  return render_template('social/profile.html', user = user, error = error)  


@bp.route('/<string:username>/edit', methods = ['GET', 'POST'])
def edit(username):
  post = get_post(id)
  error = None
  db = get_db()
  pass
  # if request.method == 'POST':
  #   title = request.form['title']
  #   body = request.form['body']

  #   if not title: error = 'Title is required'
  #   elif not body: error = 'Body cannot be empty'
  #   elif len(body) < 3: error = 'Body must have atleast 3 characters'

  #   if error is not None:
  #     flash(error)
  #   else:
  #     db.execute('UPDATE user_detail SET title = ? , body = ? WHERE post_id = ? ', (title, body, id))
  #     db.commit()

    # grab data
    # verify data
    # update database
    # redirect to profile page
  return render_template('social/edit_profile.html', post=post)


  