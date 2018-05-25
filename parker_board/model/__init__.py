from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    print('db initializing')
    db.app = app
    db.init_app(app)

