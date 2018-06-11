from flask import Flask, request, jsonify
from flask_login import LoginManager
from app.schema.resp import resp_schema


login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    import os
    if not os.environ.get('APP_SETTING'):
        os.environ['APP_SETTING'] = 'config/dev.cfg'

    app.config.from_envvar('APP_SETTING', silent=True)
    os.environ['AUTO_COMMIT'] = str(app.config['SQLALCHEMY_AUTO_COMMIT'])

    from app import model as db
    db.init_app(app)

    from app import migrate as mi
    mi.init_app(app)

    from app import schema as ma
    ma.init_app(app)

    login_manager.init_app(app)

    from app.controller.user_controller import bp as user_bp
    app.register_blueprint(user_bp)

    from app.controller.board_controller import bp as board_bp
    app.register_blueprint(board_bp)

    from app.controller.post_controller import bp as post_bp
    app.register_blueprint(post_bp)

    from app.controller.comment_controller import bp as comment_bp
    app.register_blueprint(comment_bp)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        next = request.path if request.path else '/'

        result = dict(message='Login First.', next=next)
        return jsonify(result), 400

    @app.errorhandler(422)
    def schema_validation_handler(err):
        exc = getattr(err, 'exc')
        messages = exc.messages if exc else ['Invalid request']

        result = dict(errors=messages)

        return jsonify(result), 422

    return app


