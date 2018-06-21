import flask
import datetime

from flask import Flask, request, jsonify, g
from flask_login import LoginManager, current_user
from app.model.user import User

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

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

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
        return jsonify(result), 401

    @app.errorhandler(422)
    def schema_validation_handler(err):
        exc = getattr(err, 'exc')
        messages = exc.messages if exc else ['Invalid request']

        result = dict(errors=messages)
        print(messages)
        return jsonify(result), 422

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app


