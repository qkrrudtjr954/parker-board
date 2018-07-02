import pytest
import json

from app.model.comment import Comment
from app.schema.comment import comment_create_form_schema, comment_update_form_schema

from tests.factories.comment import FakeCommentFactory
from tests.factories.post import FakePostFactory


class Describe_CommentController:
    @pytest.fixture
    def user(self, logged_in_user):
        return logged_in_user

    @pytest.fixture
    def target_post_id(self):
        post = FakePostFactory()
        return post.id

    @pytest.fixture
    def json_result(self, subject):
        return json.loads(subject.data)

    class Describe_comment_list:
        @pytest.fixture
        def target_post(self):
            post = FakePostFactory()
            post.comments = FakeCommentFactory.create_batch(20)
            return post

        @pytest.fixture
        def subject(self, target_post, user):
            resp = self.client.get('/posts/%d/comments' % target_post.id)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_댓글_수는_20개이다(self, subject):
            assert 20 == Comment.query.count()

        class Context_댓글이_없을_때:
            @pytest.fixture
            def target_post(self):
                post = FakePostFactory()
                return post

            def test_댓글이_없다면_빈매열을_반환한다(self, json_result):
                assert [] == json_result['comment_list']

        class Context_post가_없을_때:
            @pytest.fixture
            def target_post(self):
                post = FakePostFactory.build()
                return post

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

    class Describe_create:
        @pytest.fixture
        def form(self):
            comment = FakeCommentFactory.build()
            return comment

        @pytest.fixture
        def subject(self, target_post_id, form, user):
            resp = self.client.post('/posts/%d/comments' % target_post_id, data=comment_create_form_schema.dumps(form).data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_DB에_comment가_저장된다(self, json_result, form, user):
            comment_id = json_result['id']
            db_comment = Comment.query.get(comment_id)
            assert db_comment.content == form.content
            assert db_comment.user_id == user.id

        def test_post의_comment_count가_증가한다(self, json_result):
            db_comment = Comment.query.get(json_result['id'])
            assert 1 == db_comment.post.comments_count

        class Context_로그인을_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_content가_없을_때:
            @pytest.fixture
            def form(self):
                comment = FakeCommentFactory.build(content='')
                return comment

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        class Context_post가_없을_때:
            @pytest.fixture
            def target_post_id(self):
                post = FakePostFactory.build()
                return post.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

    class Describe_delete:
        @pytest.fixture
        def target_comment_id(self, user):
            comment = FakeCommentFactory(user=user, user_id=user.id)
            comment.post.comments_count = 1
            self.session.commit()
            return comment.id

        @pytest.fixture
        def subject(self, target_comment_id):
            resp = self.client.delete('/comments/%d' % target_comment_id)
            return resp

        def test_204를_반환한다(self, subject):
            assert 204 == subject.status_code

        def test_DB의_comment가_삭제된다(self, subject, target_comment_id):
            db_comment = Comment.query.get(target_comment_id)
            assert db_comment.is_deleted

        def test_post의_comment_count가_감소한다(self, subject, target_comment_id):
            db_comment = Comment.query.get(target_comment_id)
            assert 0 == db_comment.post.comments_count

        class Context_comment가_존재하지_않을_때:
            @pytest.fixture
            def target_comment_id(self, user):
                comment = FakeCommentFactory.build(user=user, user_id=user.id)
                return comment.id

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_로그인_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401를_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_본인_게시글이_아닌_경우:
            @pytest.fixture
            def target_comment_id(self):
                comment = FakeCommentFactory()
                return comment.id

            def test_401를_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_update:
        @pytest.fixture
        def update_data(self):
            return dict(content='changed content.')

        @pytest.fixture
        def target_comment(self, user):
            target_comment = FakeCommentFactory(user=user, user_id=user.id)
            self.session.commit()
            return target_comment

        @pytest.fixture
        def subject(self, update_data, target_comment):
            resp = self.client.patch('/comments/%d' % target_comment.id, data=comment_update_form_schema.dumps(update_data).data, content_type='application/json')
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_DB의_comment값이_갱신된다(self, json_result):
            db_comment = Comment.query.get(json_result['id'])

            assert db_comment.content == 'changed content.'

        class Context_이전과_데이터가_같을_때:
            @pytest.fixture
            def update_data(self, target_comment):
                return dict(content=target_comment.content)

            def test_406을_반환한다(self, subject):
                assert 406 == subject.status_code

        class Context_본인의_게시글이_아닌_경우:
            @pytest.fixture
            def target_comment(self):
                comment = FakeCommentFactory()
                self.session.commit()
                return comment

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        class Context_로그인_하지_않았을_때:
            @pytest.fixture
            def user(self, not_logged_in_user):
                return not_logged_in_user

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

        @pytest.mark.parametrize('content', ['', None])
        class Context_content가_존재하지_않을_때:
            @pytest.fixture
            def update_data(self, content):
                return dict(content=content)

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        class Context_comment가_존재하지_않을_때:
            @pytest.fixture
            def target_comment(self, user):
                comment = FakeCommentFactory.build(user=user, user_id=user.id)
                return comment

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code




