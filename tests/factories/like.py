import factory

from app.model import db
from app.model.like import Like
from tests.factories.user import FakeUserFactory
from tests.factories.post import FakePostFactory


class FakeLikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    user_id = factory.Sequence(lambda n: FakeUserFactory().id)
    post_id = factory.Sequence(lambda n: FakePostFactory().id)
    # user_id = factory.SubFactory(FakeUserFactory)
    # post_id = factory.SubFactory(FakePostFactory)

    class Meta:
        model = Like
        sqlalchemy_session = db.session
