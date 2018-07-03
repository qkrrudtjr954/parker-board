import enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.likes import Likes
from app.model.timestamp import TimestampMixin
from app.model.user import User
from app.model.comment import Comment


class PostStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Post(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    read_count = db.Column(db.Integer, nullable=False, default=0)
    comments_count = db.Column(db.Integer, nullable=False, default=0)

    status = db.Column(ChoiceType(PostStatus, impl=db.Integer()), default=PostStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)

    comments = db.relationship("Comment", backref='post', lazy='dynamic')

    likes = db.relationship("Likes", lazy='dynamic')

    @hybrid_property
    def is_deleted(self):
        return self.status == PostStatus.DELETED

    @property
    def like_count(self):
        return self.likes.filter(Likes.post_id == Post.id).count()

    def delete(self):
        self.status = PostStatus.DELETED

    def read(self):
        self.read_count = Post.read_count + 1
        db.session.commit()

    def is_owner(self, user: User):
        return self.user_id == user.id

    def like(self, user: User):
        liked = self._get_liked(user.id)

        if not liked:
            like = Likes(user_id=user.id, post_id=self.id)
            db.session.add(like)
            db.session.commit()

    def unlike(self, user: User):
        liked = self._get_liked(user.id)

        if liked:
            db.session.delete(liked)
            db.session.commit()

    def _get_liked(self, user_id):
        return self.likes.filter(Likes.user_id == user_id).first()

    def increase_comments_count(self):
        self.comments_count = Post.comments_count + 1

    def decrease_comments_count(self):
        self.comments_count = Post.comments_count - 1

    def __repr__(self):
        return "<Post title: %s, content: %s, description: %s, status: %s," \
               " created_at: %s, updated_at: %s>"\
               % (self.title, self.content, self.description, self.status,
                  self.created_at, self.updated_at)

