import pytest
from tests.factories.comment import FakeCommentFactory
from app.model.comment import Comment



@pytest.fixture(scope='function')
def fcomment(tsession):
    FakeCommentFactory._meta.sqlalchemy_session = tsession
    yield FakeCommentFactory()




