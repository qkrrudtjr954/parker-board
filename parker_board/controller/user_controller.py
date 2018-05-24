from flask import Blueprint, current_app


user = Blueprint('user', __name__, url_prefix='/users')


@user.route('/', methods=['POST'])
def register():
    pass


@user.route('/login', methods=['POST'])
def login():
    pass


@user.route('/logout', methods=['POST'])
def logout():
    pass
