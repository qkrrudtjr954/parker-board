from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/parkerdev'
    app.config['SECRET_KEY'] = 'some_secret_key'

    from parker_board import model as db
    db.init_app(app)

    from parker_board import migrate
    migrate.init_app(app)

    from parker_board import schema as ma
    ma.init_app(app)

    from parker_board.controller.user_controller import bp as user_bp
    app.register_blueprint(user_bp)

    from parker_board.controller.board_controller import bp as board_bp
    app.register_blueprint(board_bp)

    @app.route('/')
    def index():
        return 'hello world'

    return app


