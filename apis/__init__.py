from .db import init_app

import os

from flask import Flask, g

app = Flask(__name__, instance_relative_config = True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'api.sqlite')
)

# if test_config is None:
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     app.config.from_mapping(test_config)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/hello')
def hello():
    return {
        "loggedInUser": g.user
    }

from . import db
db.init_app(app);

from . import auth
from . import blog

app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)