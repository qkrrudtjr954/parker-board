import enum
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ChoiceType

from app.model import db
from app.model.like import Like
from app.model.user import User
from app.model.comment import Comment


class PostStatus(enum.Enum):
    NORMAL = 0
    DELETED = 2


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    readcount = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(ChoiceType(PostStatus, impl=db.Integer()), default=PostStatus.NORMAL)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship("User")

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)

    comments = db.relationship("Comment", backref='post', lazy='dynamic')

    likes = db.relationship("Like", lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_comments(self, page, per_page):
        return self.comments.filter(
            ~Comment.is_deleted
        ).order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    def refresh_update_time(self):
        self.updated_at = datetime.utcnow()

    @hybrid_property
    def is_deleted(self):
        return self.status == PostStatus.DELETED

    @property
    def like_count(self):
        return Like.query.filter(Like.post_id == self.id).count()

    def delete(self):
        self.status = PostStatus.DELETED

    def read(self):
        self.readcount = self.readcount+1
        # self.readcount = Post.readcount + 1

        db.session.commit()

    def is_same_data(self, dict_data):
        same = True

        if 'title' in dict_data and self.title != dict_data['title']:
            same = False
        if 'content' in dict_data and self.content != dict_data['content']:
            same = False
        if 'description' in dict_data and self.description != dict_data['description']:
            same = False

        return same

    def like(self, user: User):
        liked = self.likes.filter(Like.user_id == user.id).first()
        # liked = Like.query.filter(Like.user_id == user.id, Like.post_id == self.id).first()

        if not liked:
            like = Like(user_id=user.id, post_id=self.id)
            # self.likes.add(like)
            db.session.add(like)
            db.session.commit()

    def unlike(self, user: User):
        liked = self.likes.filter(Like.user_id == user.id).first()

        if liked:
            db.session.delete(liked)
            db.session.commit()

    def __repr__(self):
        return "<Post title: %s, content: %s, description: %s, status: %s," \
               " created_at: %s, updated_at: %s>"\
               % (self.title, self.content, self.description, self.status,
                  self.created_at, self.updated_at)

