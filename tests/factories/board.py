import factory
from parker_board.model import db
from parker_board.model.board import Board
from datetime import datetime


class FakeBoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    status = 0

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Board
        sqlalchemy_session = db.session


class FakeBoardAndUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    user = factory.SubFactory('tests.factories.user.FakeUserFactory')
    status = 0

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Board
        sqlalchemy_session = db.session








