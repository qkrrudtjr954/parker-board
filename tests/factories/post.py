import factory
from parker_board.model import db
from parker_board.model.post import Post
from datetime import datetime


class FakePostFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    content = factory.Faker('sentence')
    description = factory.Faker('sentence')
    status = 0

    user = factory.SubFactory('tests.factories.board.FakeUserFactory')
    board = factory.SubFactory('tests.factories.board.FakeBoardFactory')

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Post
        sqlalchemy_session = db.session
