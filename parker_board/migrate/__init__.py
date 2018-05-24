from flask_migrate import Migrate, Manager
from parker_board.model import db


migrate = Migrate(db=db)


def init_app(app):
    migrate.init_app(app=app)


