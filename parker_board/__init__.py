from flask import Flask
from flask.ext.session import Session

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/parkerdev'
    app.config['SECRET_KEY'] = 'dev'

    Session(app)

    from parker_board import model as db
    db.init_app(app)

    from parker_board import migrate
    migrate.init_app(app)

    from parker_board import schema as ma
    ma.init_app(app)


    from parker_board.controller.user_controller import bp as user_bp
    app.register_blueprint(user_bp)

    @app.route('/')
    def index():
        return 'hello world'

    return app


