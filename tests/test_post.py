import pytest
import json
from tests.factories.post import FakePostFactory
from tests.factories.board import FakeBoardFactory
from app.model.post import Post, PostStatus
from app.schema.post import post_schema, before_create_post_schema
from app.schema.user import before_login_schema


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

        resp = tclient.post('/boards/%d/posts' % fpost_build.board.id, data=post_schema.dumps(fpost_build).data, content_type='application/json')
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

        resp = tclient.post('/boards/%d/posts' % fpost_build.board_id, data=before_create_post_schema.dumps(dict(title='helloworld', content='funny world')).data, content_type='application/json')
        print(resp.data)

        assert resp.status_code == 200


class TestUpdatePost:
    def test_update_no_login(self, tclient, fpost_create, tsession):
        assert tsession.query(Post).one()

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost_create.id, data=post_schema.dumps(update_data).data, content_type='application/json')
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
        resp = tclient.patch('/posts/%d' % fpost_create.id, data=post_schema.dumps(update_data).data, content_type='application/json')

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
        resp = tclient.patch('/posts/%d' % update_post.id, data=post_schema.dumps(update_data).data, content_type='application/json')

        assert resp.status_code == 401
        assert resp.data == b'No Authentication.'


class TestDeletePost:
    def test_delete_post(self, tsession, tclient, fpost_create):
        assert tsession.query(Post).one()

        resp = tclient.post('/users/login', data=before_login_schema.dumps(fpost_create.user).data, content_type='application/json')
        assert resp.status_code == 200

        resp = tclient.delete('/posts/%d' % fpost_create.id, content_type='application/json')
        assert resp.status_code == 200
        assert fpost_create.status == PostStatus.DELETED

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


class TestReadPost:
    def test_read_post(self, fpost_create, tsession, tclient):
        assert tsession.query(Post).one()

        login_user = fpost_create.user

        resp = tclient.post('/users/login', data=before_login_schema.dumps(login_user).data, content_type='application/json')

        assert resp.status_code == 200

        resp = tclient.get('/posts/%d' % fpost_create.id, content_type='application/json')
        assert resp.status_code == 200

        result = json.loads(resp.data)

        assert resp.status_code == 200
        assert result['post']['content'] == fpost_create.content

    def test_read_no_login(self, fpost_create, tsession, tclient):
        assert tsession.query(Post).one()

        resp = tclient.get('/posts/%d' % fpost_create.id, content_type='application/json')
        result = json.loads(resp.data)

        assert resp.status_code == 400
        assert result['message'] == 'Login First.'
