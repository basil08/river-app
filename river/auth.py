import functools 

from flask import (
  Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from river.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/a')

@bp.route('/signup', methods = ['GET', 'POST'])
def signup():
  if request.method == 'POST':
    # grab data

    # non-optional
    name = request.form['name']
    username = request.form['username']
    email_id = request.form['email_id']
    password = request.form['password']

    # optional
    bio = request.form['bio']
    relationship_status = request.form['relationship_status']
    location = request.form['location']

    # verify data
    db = get_db()
    error = None

    if not name: error = 'Your name is required'
    elif len(name) <= 2: error = 'Your name should have atleast 3 characters'
    elif not username: error = 'Your username is required'
    elif db.execute('SELECT user_id FROM user_detail WHERE username = ? ', (username,)).fetchone() is not None:
      error = "User {} already exists! Try a different username".format(username)
    
    # what if optional fields are white spaces?

    # insert data in db
    if error is None:

      db.execute(
        'INSERT INTO user_detail (name, username, password, email_id, bio, relationship_status, location) \
          VALUES (?,?,?,?,?,?,?)',(name, username, generate_password_hash(password), email_id, bio, relationship_status, location)
      )
      db.commit()
      session.clear()
      return redirect(url_for('auth.login'))

    flash(error)

  return render_template('auth/signup.html')


@bp.route('/login', methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':

    # user can login via either username or email id
    username = request.form['username']
    email_id = request.form['email_id']
    password = request.form['password']

    db = get_db()
    error, user = None, None

    if username:
      user = db.execute('SELECT * FROM user_detail WHERE username = ?', (username,)).fetchone()
    elif email_id:
      user = db.execute('SELECT * FROM user_detail WHERE email_id = ?', (email_id,)).fetchone()
    else:
      error = 'No credential provided. Enter your username/email id'

    if username or email_id:
      if user is not None:
        if not check_password_hash(user['password'], password):
          error = 'Incorrect Password'
      else:
        error = 'Incorrect/Non-existent User'


    if error is None:
      session.clear()
      session['user_id'] = user['user_id']
      return redirect(url_for('user.home'))

    flash(error)
  
  return render_template('auth/login.html')


# As user id is stored in the session, it will be available on subsequent requests
# This functions runs before processing any request and loads the current user information 
# from database into the global g object
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user_detail WHERE user_id = ?', (user_id,)
    ).fetchone()
  
@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    return view(**kwargs)
  
  return wrapped_view
