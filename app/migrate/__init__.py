from flask_migrate import Migrate
from app.model import db


migrate = Migrate(db=db)

def init_app(app):
    print('init migrate')
    migrate.init_app(app=app)

