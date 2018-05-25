from flask_marshmallow import Marshmallow

ma = Marshmallow()

def init_app(app):
    print('init marshmallow.')
    ma.init_app(app)