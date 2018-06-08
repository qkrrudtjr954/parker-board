import logging
import sys

import pytest
from app import create_app

from app.model import db

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@pytest.fixture(scope='session')
def tapp():
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def tdb(tapp):

    db.init_app(tapp)
    return db


@pytest.fixture(scope='session')
def tclient(tapp):
    client = tapp.test_client()
    return client


@pytest.fixture(scope='function')
def tsession(tdb):
    session = tdb.session
    yield session
    session.rollback()