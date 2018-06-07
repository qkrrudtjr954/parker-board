import factory
from app.model import db
from app.model.comment import Comment
from datetime import datetime


class FakeCommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    content = factory.Faker('sentence')
    status = 0

    user = factory.SubFactory('tests.factories.user.FakeUserFactory')
    post = factory.SubFactory('tests.factories.post.FakePostFactory')

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Comment
        sqlalchemy_session = db.session
