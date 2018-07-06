import factory
from app.model import db
from app.model.board import Board, BoardStatus
from tests.factories.user import UserFactory
from datetime import datetime


class BoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    status = BoardStatus.NORMAL

    user = factory.SubFactory(UserFactory)

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Board
        sqlalchemy_session = db.session

