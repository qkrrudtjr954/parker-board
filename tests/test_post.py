import pytest
import json

from app.model.post import Post
from app.schema.post import post_create_form_schema, post_update_form_schema
from app.schema.user import before_login_schema

from tests.factories.post import FakePostFactory
from tests.factories.board import FakeBoardFactory
from tests.factories.user import FakeUserFactory

from flask_login import current_user, login_user


@pytest.fixture(scope='function')
def fboard(tsession):
    board = FakeBoardFactory()
    tsession.flush()
    return board


@pytest.fixture(scope='function')
def fposts(tsession):
    posts = FakePostFactory.create_batch(10)
    tsession.flush()
    return posts


@pytest.fixture(scope='function')
def fpost_build(tsession):
    post = FakePostFactory.build()
    return post


@pytest.fixture(scope='function')
def fpost_create(tsession):
    post = FakePostFactory()
    tsession.flush()
    return post


class TestCreatePost:
    def test_create_no_login(self, tclient, fpost_build, tsession):
        tsession.add(fpost_build.user)
        tsession.add(fpost_build.board)
        tsession.flush()

        resp = tclient.post('/boards/%d/posts' % fpost_build.board.id, data=post_create_form_schema.dumps(fpost_build).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'

    def test_create_post(self, tclient, fpost_build, tsession):
        tsession.add(fpost_build.user)
        tsession.add(fpost_build.board)
        tsession.flush()

        # login
        login_user = fpost_build.user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.post('/boards/%d/posts' % fpost_build.board_id, data=post_create_form_schema.dumps(dict(title='helloworld', content='funny world')).data, content_type='application/json')
        print(resp.data)

        assert resp.status_code == 200


class TestUpdatePost:
    def test_update_no_login(self, tclient, fpost_create, tsession):
        assert tsession.query(Post).one()

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost_create.id, data=post_update_form_schema.dumps(update_data).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'

    def test_update_post(self, tclient, fpost_create, tsession):
        assert tsession.query(Post).one()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(fpost_create.user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['user']['email'] == fpost_create.user.email

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost_create.id, data=post_update_form_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 200
        assert fpost_create.title == 'changed title'
        assert fpost_create.content == 'changed content'

    def test_update_no_auth(self, tclient, fposts):
        login_user = fposts[0].user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['user']['email'] == login_user.email

        update_post = fposts[1]

        update_data = dict(title='changed title', content='changed content')
        resp = tclient.patch('/posts/%d' % update_post.id, data=post_update_form_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'


class TestDeletePost:
    def test_delete_post(self, tsession, tclient, fpost_create):
        assert tsession.query(Post).one()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(fpost_create.user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.delete('/posts/%d' % fpost_create.id, content_type='application/json')
        assert resp.status_code == 200
        assert fpost_create.is_deleted

    def test_delete_no_login(self, tsession, tclient, fpost_create):
        assert tsession.query(Post).one()

        resp = tclient.delete('/posts/%d' % fpost_create.id, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'

    def test_delete_no_auth(self, tsession, tclient, fposts):
        login_user = fposts[0].user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['user']['email'] == login_user.email

        delete_post = fposts[1]

        resp = tclient.delete('/posts/%d' % delete_post.id, content_type='application/json')
        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'


@pytest.fixture
def user(tclient, tsession):
    user = FakeUserFactory()

    resp = tclient.post('/users/login', data=before_login_schema.dump(user).data)
    print(resp.headers)
    return user

def test_login(user):
    print(user)
    pass


@pytest.fixture
def credentials(user):
    return [('Authentication', user.get_auth_token())]


# class Describe_PostController:
#     class Describe_PostList:
#         class Context_when_user_logged_in:
#             class Context_when_board_not_exist:
#                 def test_is_expected_404(self, tclient):
#                     pass
#
#             class Context_when_board_exist:
#                 def test_is_expected_200(self, tclient):
#                     board = FakeBoardFactory.create(posts=FakePostFactory.create_batch(10))
#
#                     resp = tclient.get('/boards/%d/posts' % board.id)
#                     print(resp.data)
#
#                     assert resp.status_code == 200
#
#         class Context_when_user_not_logged_in:
#             pass

class TestPostList:
    def test_post_list(self, fpost_create, tsession, tclient):
        assert tsession.query(Post).one()

        login_user = fpost_create.user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')

        assert resp.status_code == 200

        resp = tclient.get('/posts/%d' % fpost_create.id, content_type='application/json')
        assert resp.status_code == 200

    def test_read_no_login(self, fpost_create, tsession, tclient):
        assert tsession.query(Post).one()

        resp = tclient.get('/posts/%d' % fpost_create.id, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'
