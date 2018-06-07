import pytest
from tests.factories.post import FakeUserAndPostFactory, FakePostFactory
from tests.factories.board import FakeBoardAndUserFactory
from tests.factories.user import FakeUserFactory
from app.model.user import User
from app.model.board import Board
from app.model.post import Post
from app.schema.post import post_schema
from app.schema.user import login_schema
from app.schema.resp import resp_schema


@pytest.fixture(scope='function')
def fboard(tsession):
    board = FakeBoardAndUserFactory()
    tsession.flush()
    return board

@pytest.fixture(scope='function')
def fpost(fboard, tsession):
    post = FakeUserAndPostFactory.build(board_id=fboard.id, board=fboard)
    return post


class TestCreatePost:
    def test_create_no_login(self, tclient, fpost, tsession):
        assert tsession.query(User).one()
        assert tsession.query(Board).one()
        assert Post.query.count() == 0


        resp = tclient.post('/boards/%d/posts'%fpost.board_id, data=post_schema.dumps(fpost).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 400
        assert result['status_code'] == 400
        assert result['errors']['error'] == 'Login First.'

    # def test_create_post(self, tclient, fpost, tsession):
    #     assert tsession.query(User).one()
    #     assert tsession.query(Board).one()
    #     assert Post.query.count() == 0
    #
    #     # login
    #     login_user = User.query.first()
    #
    #     resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
    #     result = resp_schema.loads(resp.data.decode()).data
    #     print(result)
    #     assert result['status_code'] == 200
    #
    #     resp = tclient.post('/boards/%d/posts' % fpost.board_id, data=post_schema.dumps(fpost).data, content_type='application/json')
    #     result = resp_schema.loads(resp.data.decode()).data
    #
    #     assert result['status_code'] == 200
    #     assert Post.query.one()


class TestUpdatePost:
    def test_update_no_login(self, tclient, fpost, tsession):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost.id, data=post_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['status_code'] == 400
        assert result['errors']['error'] == 'Login First.'

    def test_update_post(self, tclient, fpost, tsession):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        resp = tclient.post('/users/login', data=login_schema.dumps(fpost.user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200
        assert result['status_code'] == 200

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost.id, data=post_schema.dumps(update_data).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 200
        assert result['status_code'] == 200
        assert fpost.title == 'changed title'
        assert fpost.content == 'changed content'

    def test_update_no_auth(self, tclient, fpost, tsession):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        login_user = FakeUserFactory()
        tsession.add(login_user)
        tsession.flush()

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200
        assert result['status_code'] == 200

        update_data = dict(title='changed title', content='changed content', comments=[])
        resp = tclient.patch('/posts/%d' % fpost.id, data=post_schema.dumps(update_data).data,
                             content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 401
        assert result['status_code'] == 401
        assert result['errors']['error'] == 'Can\'t update.'


class TestDeletePost:
    def test_delete_post(self, tsession, tclient, fpost):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        resp = tclient.post('/users/login', data=login_schema.dumps(fpost.user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200
        assert result['status_code'] == 200

        resp = tclient.delete('/posts/%d' % fpost.id, content_type='application/json')
        assert resp.status_code == 204
        assert resp.status_code == 204

    def test_delete_no_login(self, tsession, tclient, fpost):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        resp = tclient.delete('/posts/%d' % fpost.id, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data

        assert resp.status_code == 400
        assert result['status_code'] == 400
        assert result['errors']['error'] == 'Login First.'

    def test_delete_no_auth(self, tsession, tclient, fpost):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        login_user = FakeUserFactory()
        tsession.add(login_user)
        tsession.flush()

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200
        assert result['status_code'] == 200

        resp = tclient.delete('/posts/%d' % fpost.id, content_type='application/json')
        assert resp.status_code == 401
        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 401
        assert result['errors']['error'] == 'Can\'t delete.'


class TestReadPost:
    def test_read_post(self, fpost, tsession, tclient):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        login_user = fpost.user

        resp = tclient.post('/users/login', data=login_schema.dumps(login_user).data, content_type='application/json')
        result = resp_schema.loads(resp.data.decode()).data
        assert resp.status_code == 200
        assert result['status_code'] == 200

        resp = tclient.get('/posts/%d' % fpost.id, content_type='application/json')
        assert resp.status_code == 200

        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 200
        assert result['data']['content'] == fpost.content

    def test_read_no_login(self, fpost, tsession, tclient):
        tsession.add(fpost)
        tsession.flush()
        assert tsession.query(Post).one()

        resp = tclient.get('/posts/%d' % fpost.id, content_type='application/json')
        assert resp.status_code == 400

        result = resp_schema.loads(resp.data.decode()).data
        assert result['status_code'] == 400
        assert result['errors']['error'] == 'Login First.'