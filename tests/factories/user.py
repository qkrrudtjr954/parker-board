import factory
from app.model import db
from app.model.user import User, UserStatus
from datetime import datetime
from werkzeug.security import generate_password_hash




class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n+1)
    email = factory.Faker('email')
    password = factory.Faker('password')

    status = UserStatus.ACTIVE

    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    class Meta:
        model = User
        sqlalchemy_session = db.session

