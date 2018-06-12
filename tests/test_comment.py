import pytest
import json

from app.model.comment import CommentStatus
from app.schema.user import before_login_schema
from app.schema.comment import comment_create_form_schema, comment_update_form_schema
from tests.factories.comment import FakeCommentFactory
from tests.factories.post import FakePostFactory


@pytest.fixture(scope='function')
def fpost(tsession):
    post = FakePostFactory()
    tsession.flush()

    return post


@pytest.fixture(scope='function')
def fcomment(tsession):
    comment = FakeCommentFactory()
    tsession.flush()

    return comment


@pytest.fixture(scope='function')
def fcomments(tsession):
    comments = FakeCommentFactory.create_batch(5)
    tsession.flush()

    return comments


def login(client, user):
    resp = client.post('/users/login', data=before_login_schema.dump(user).data)
    return resp


class TestCreateComment:
    def test_create_comment(self, tclient, fpost):
        resp = login(tclient, fpost.user)
        assert resp.status_code == 200

        comment = FakeCommentFactory.build()
        resp = tclient.post('/posts/%d/comments' % fpost.id, data=comment_create_form_schema.dump(comment).data)

        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['content'] == comment.content

    def test_create_comment_no_content(self, tclient, fpost):
        resp = login(tclient, fpost.user)
        assert resp.status_code == 200

        comment = FakeCommentFactory.build(content='asd')
        resp = tclient.post('/posts/%d/comments' % fpost.id, data=comment_create_form_schema.dump(comment).data)
        result = json.loads(resp.data)

        assert resp.status_code == 422
        assert result['errors']['content'] == ['Contents length must more than 15.']


class TestUpdateComment:
    def test_update_comment(self, tclient, fcomment):
        resp = login(tclient, fcomment.user)
        assert resp.status_code == 200

        update_data = dict(content='changed content')
        resp = tclient.patch('/comments/%d' % fcomment.id, data=comment_update_form_schema.dump(update_data).data)
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['content'] == fcomment.content

    def test_update_comment_no_auth(self, tclient, fcomments):
        resp = login(tclient, fcomments[0].user)
        assert resp.status_code == 200

        update_data = dict(content='changed content')
        resp = tclient.patch('/comments/%d' % fcomments[1].id, data=comment_update_form_schema.dump(update_data).data)

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'


class TestDeleteComment:
    def test_delete_comment(self, tclient, fcomment):
        resp = login(tclient, fcomment.user)
        assert resp.status_code == 200

        resp = tclient.delete('/comments/%d' % fcomment.id)
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['content'] == fcomment.content
        assert fcomment.status == CommentStatus.DELETED

    def test_delete_comment_no_auth(self, tclient, fcomments):
        user = fcomments[0].user
        comment = fcomments[1]

        resp = login(tclient, user)
        assert resp.status_code == 200

        resp = tclient.delete('/comments/%d' % comment.id)

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'
        assert fcomments[1].status != CommentStatus.DELETED

    def test_delete_comment_no_data(self, tclient, fcomment):
        resp = login(tclient, fcomment.user)
        assert resp.status_code == 200

        resp = tclient.delete('/comments/%d' % 400)

        assert resp.status_code == 400
        assert resp.data == b'No Comment.'







