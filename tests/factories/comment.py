import factory
import factory.fuzzy
from app.model import db
from app.model.comment import Comment, CommentStatus
from datetime import datetime

from tests.factories.user import UserFactory


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Comment
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n+1)
    content = factory.Faker('sentence')

    # status = factory.fuzzy.FuzzyChoice([CommentStatus.NORMAL, CommentStatus.DELETED])
    status = CommentStatus.NORMAL

    user = factory.SubFactory(UserFactory)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

