import factory
from parker_board.model import db
from parker_board.model.user import User
from datetime import datetime


class FakeUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    email = factory.Faker('email')
    password = factory.Faker('password')
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model=User
        sqlalchemy_session = db.session
