import os

from flask import Flask

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


  @app.route('/')
  def hello(): return '<h1>River</h1><h3><em>Where ideas meet</em></h3>'

  return app