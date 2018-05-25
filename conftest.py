import pytest
from parker_board import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app(None)
    app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/parkertest'
    app.config['TESTING']=True

    return app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()