import pytest
from parker_board import create_app


@pytest.fixture(scope='session')
def tapp():
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def client(tapp):
    yield tapp.test_client()
    print('end client')