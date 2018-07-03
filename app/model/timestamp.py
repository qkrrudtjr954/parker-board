from datetime import datetime

from app.model import db


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())
