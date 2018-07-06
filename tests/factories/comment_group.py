from datetime import datetime

import factory

from app.model import db
from app.model.commnet_group import CommentGroup
from tests.factories.comment import CommentFactory


class CommentGroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CommentGroup
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n+1)
    comments = factory.List([
        factory.SubFactory(CommentFactory) for _ in range(10)
    ])
    created_at = factory.LazyFunction(datetime.utcnow)




