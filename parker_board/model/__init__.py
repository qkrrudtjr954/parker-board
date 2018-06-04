from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': False})


def init_app(app):
    print('db initializing')
    db.app = app
    db.init_app(app)
    print(db.session.autoflush)
    print(db.session.autocommit)

