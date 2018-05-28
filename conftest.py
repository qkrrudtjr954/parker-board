import pytest
from parker_board import create_app


@pytest.fixture(scope='session')
def tapp():
    app = create_app(None)
    # app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost/parkertest'
    # app.config['SECRET_KEY'] = 'testing'
    # app.config['TESTING']=True

    return app


@pytest.fixture(scope='session')
def client(tapp):
    return tapp.test_client()