from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/parkerdev'

    from parker_board.model import db
    db.init_app(app)

    from parker_board.migrate import migrate
    migrate.init_app(app)

    # from yourapplication.views.admin import admin
    # from yourapplication.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)

    return app
