import factory
from app.model import db
from app.model.post import Post, PostStatus
from datetime import datetime
from tests.factories.board import BoardFactory
from tests.factories.comment_group import CommentGroupFactory
from tests.factories.user import UserFactory


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    content = factory.Faker('sentence', nb_words=20)
    description = factory.Faker('sentence')
    status = PostStatus.NORMAL

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Post
        sqlalchemy_session = db.session


#temp
class HasManyCommentPostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n+1)

    title = factory.Faker('sentence')
    content = factory.Faker('sentence', nb_words=20)
    description = factory.Faker('sentence')
    status = factory.Iterator([PostStatus.NORMAL, PostStatus.DELETED])

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)

    comment_groups = factory.List([
        factory.SubFactory(CommentGroupFactory) for _ in range(10)
    ])

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)




