import factory
from parker_board.model import db
from parker_board.model.board import Board
from datetime import datetime


class FakeBoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n:n+1)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')

    # user_id

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = Board
        sqlalchemy_session = db.session








