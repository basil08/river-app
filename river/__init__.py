import os

from flask import Flask, render_template

def create_app(test_config=None):
  """
  Application factory
  """
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'river.sqlite'),
  )  

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # attach database
  from . import db
  db.init_app(app)

  # attach blueprints, views etc
  from . import auth
  app.register_blueprint(auth.bp)

  from . import user
  app.register_blueprint(user.bp)

  from . import post
  app.register_blueprint(post.bp)

  @app.route('/')
  def index():
    return render_template('index.html')

  return app