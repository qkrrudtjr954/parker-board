import factory
from app.model import db
from app.model.comment import Comment
from datetime import datetime
from tests.factories.user import FakeUserFactory
from tests.factories.post import FakePostFactory


class FakeCommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    content = factory.Faker('sentence')
    status = 0

    user = factory.SubFactory(FakeUserFactory)
    post = factory.SubFactory(FakePostFactory)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Comment
        sqlalchemy_session = db.session
