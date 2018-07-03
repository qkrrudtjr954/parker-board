from flask import Flask, request
from app.model.user import User
from app.schema.error import default_message_error_schema, default_messages_error_schema


def create_app():
    app = Flask(__name__)

    import os
    if not os.environ.get('APP_SETTING'):
        os.environ['APP_SETTING'] = 'config/dev.cfg'

    app.config.from_envvar('APP_SETTING', silent=True)

    from app import model as db
    db.init_app(app)

    from app import migrate as mi
    mi.init_app(app)

    from app import schema as ma
    ma.init_app(app)

    from app.controller.user_controller import login_manager
    login_manager.init_app(app)

    from app.controller.user_controller import bp as user_bp
    app.register_blueprint(user_bp)

    from app.controller.board_controller import bp as board_bp
    app.register_blueprint(board_bp)

    from app.controller.post_controller import bp as post_bp
    app.register_blueprint(post_bp)

    from app.controller.comment_controller import bp as comment_bp
    app.register_blueprint(comment_bp)

    @app.errorhandler(422)
    def schema_validation_handler(err):
        exc = getattr(err, 'exc')
        messages = exc.messages if exc else ['Invalid request']
        result = dict(messages=messages)
        return default_messages_error_schema.jsonify(result), 422

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    return app


