import functools 

from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from river.db import get_db

bp = Blueprint('user', __name__, url_prefix='/u')

@bp.route('/<string:username')
def profile(username):
  error = None
  db = get_db()
  user = db.execute('
  SELECT * FROM user_detail WHERE username = ?', (username,)
  ).fetchone()

  if not user:
    error = 'Error. User @{} does not exist.'.format(username)
    flash(error)

  # template checks if error is not None
  # accordingly, fills the table
  return render_template('social/profile.html', user = user, error = error)  



@bp.route('/<string:username/edit', methods = ['GET', 'POST'])
def edit(username):
  if request.method == 'POST':
    error = None
    db = get_db()
    # grab data
    # verify data
    # update database
    # redirect to profile page
    flash(error)
  return render_template('social/edit_profile.html')


  