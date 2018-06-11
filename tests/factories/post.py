import factory
from app.model import db
from app.model.post import Post, PostStatus
from datetime import datetime
from tests.factories.board import FakeBoardFactory
from tests.factories.user import FakeUserFactory



class FakePostFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    content = factory.Faker('sentence')
    description = factory.Faker('sentence')
    status = PostStatus.NORMAL

    user = factory.SubFactory(FakeUserFactory)
    board = factory.SubFactory(FakeBoardFactory)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Post
        sqlalchemy_session = db.session



