import pytest
from app import create_app
from app.model import db
from tests.factories.user import FakeUserFactory
from app.model.user import User


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
    db.session.autocommit = False
    db.session.autoflush = False
    session = db.session
    yield session
    session.rollback()


def test_app(tapp):
    assert tapp.config['TESTING']
    assert tapp.config['SQLALCHEMY_DATABASE_URI']=='mysql://root:root@localhost/parkertest'


def test_session(tsession):
    FakeUserFactory()
    assert tsession.query(User).count() == 1


def test_session_rollback(tsession):
    assert tsession.query(User).count() == 0
