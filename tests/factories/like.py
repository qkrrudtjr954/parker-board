import factory

from app.model import db
from app.model.likes import Likes
from tests.factories.user import UserFactory
from tests.factories.post import PostFactory


class LikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    user_id = factory.Sequence(lambda n: UserFactory().id)
    post_id = factory.Sequence(lambda n: PostFactory().id)
    # user_id = factory.SubFactory(FakeUserFactory)
    # post_id = factory.SubFactory(FakePostFactory)

    class Meta:
        model = Likes
        sqlalchemy_session = db.session
