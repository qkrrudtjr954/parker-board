import pytest
from parker_board import create_app
from parker_board.model import db
from tests.factories.user import FakeUserFactory
from parker_board.model.user import User


@pytest.fixture(scope='session')
def tapp():
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def tclient(tapp):
    client = tapp.test_client()
    return client


@pytest.fixture(scope='function')
def tsession(tapp):
    session = db.session
    yield session
    session.rollback()
    session.close()
    print('session rollback!')


def test_app(tapp):
    assert tapp.config['TESTING']


def test_session(tsession, fuser):
    print(fuser)
    assert tsession.query(User).count() == 1


def test_session_rollback(tsession):
    assert tsession.query(User).count() == 0

