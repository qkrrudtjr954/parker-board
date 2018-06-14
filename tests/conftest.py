import logging
import sys

import pytest
from app import create_app

from app.model import db
from app.schema.user import before_login_schema
from tests.factories.user import FakeUserFactory

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def tdb(app):

    db.init_app(app)
    return db


@pytest.fixture(scope='session')
def tclient(app):
    client = app.test_client()
    return client


@pytest.fixture(scope='function')
def tsession(tdb):
    session = tdb.session
    yield session
    session.rollback()


@pytest.fixture(scope='function')
def session(tdb):
    _session = tdb.session
    yield _session
    _session.rollback()


@pytest.fixture
def logged_in_user(client, tsession):
    user = FakeUserFactory.create()
    tsession.flush()

    resp = client.post('/users/login', data=before_login_schema.dumps(user).data, content_type='application/json')
    assert 200 == resp.status_code

    return user


# autouse를 사용하면 모든 픽스쳐는 해당 함수를 사용한다.
# client_class를 로드하면 client 객체를 사용할 수 있다. -> tclient는 사용하지 않아도 됨
@pytest.fixture(autouse=True)
def init(request, client_class, session):
    if request.cls is not None:
        request.cls.session = session


