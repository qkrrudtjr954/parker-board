import os

from flask import current_app
from flask_sqlalchemy import SQLAlchemy

auto_commit = os.environ.get('AUTO_COMMIT', 'False') == 'True'
db:SQLAlchemy = SQLAlchemy(session_options={'autocommit': auto_commit, 'autoflush': False})


def init_app(app):
    print('db initializing')
    db.app = app
    db.init_app(app)

