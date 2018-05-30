from flask import Flask
from flask_login import LoginManager


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_envvar('APP_SETTING', silent=True)

    from parker_board import model as db
    db.init_app(app)

    from parker_board import migrate as mi
    mi.init_app(app)

    from parker_board import schema as ma
    ma.init_app(app)

    login_manager.init_app(app)

    from parker_board.controller.user_controller import bp as user_bp
    app.register_blueprint(user_bp)

    from parker_board.controller.board_controller import bp as board_bp
    app.register_blueprint(board_bp)

    from parker_board.controller.post_controller import bp as post_bp
    app.register_blueprint(post_bp)

    from parker_board.controller.comment_controller import bp as comment_bp
    app.register_blueprint(comment_bp)

    @app.route('/')
    def index():
        return 'hello world'

    return app


