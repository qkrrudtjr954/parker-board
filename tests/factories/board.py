import factory
from app.model import db
from app.model.board import Board
from tests.factories.user import FakeUserFactory
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
    user = factory.SubFactory(FakeUserFactory)
    status = 0

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Board
        sqlalchemy_session = db.session








