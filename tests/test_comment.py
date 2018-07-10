import pytest
import json

from app.model.comment import Comment
from app.schema.comment import comment_create_form_schema, layer_comment_create_form
from tests.factories.comment import CommentFactory
from tests.factories.comment_group import CommentGroupFactory
from tests.factories.post import PostFactory, HasManyCommentPostFactory
from tests.factories.user import UserFactory


class Describe_CommentController:
    @pytest.fixture
    def user(self, logged_in_user):
        return logged_in_user

    @pytest.fixture
    def json_result(self, subject):
        return json.loads(subject.data)

    class Describe_comment_list:
        @pytest.fixture
        def target_post(self):
            post = HasManyCommentPostFactory()
            return post

        @pytest.fixture
        def subject(self, target_post, user):
            resp = self.client.get('/posts/%d/comments' % target_post.id)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_comment_list를_반환한다(self, json_result):
            assert 'comment_list' in json_result

        def test_total을_반환한다(self, json_result):
            assert 'total' in json_result
            # group 10개에 댓글 10개 씩
            assert 100 == json_result['total']

    class Describe_create_comment:
        @pytest.fixture
        def target_post(self):
            post = PostFactory()
            return post

        @pytest.fixture
        def comment_obj(self):
            comment = CommentFactory.build()
            return comment

        @pytest.fixture
        def subject(self, target_post, comment_obj, user):
            resp = self.client.post('/posts/%d/comments' % target_post.id, data=comment_create_form_schema.dump(comment_obj).data)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_comment가_db에_저장된다(self, comment_obj, json_result):
            new_comment = Comment.query.get(json_result['id'])
            assert new_comment.content == comment_obj.content

        @pytest.mark.parametrize('content', ['', None])
        class Context_content가_없을_때:
            @pytest.fixture
            def comment_obj(self, content):
                comment = CommentFactory.build(content=content)
                return comment

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('content', ['짧은 댓글', '짧다짧아~'])
        class Context_content가_짧을_때:
            @pytest.fixture
            def comment_obj(self, content):
                comment = CommentFactory.build(content=content)
                return comment

            def test_422를_반환한다(self, subject):
                assert 422 == subject.status_code

    class Describe_create_layer_comment:
        @pytest.fixture
        def target_post(self):
            post = PostFactory()
            return post

        @pytest.fixture
        def target_comment_group(self, target_post):
            comment_group = CommentGroupFactory(post_id=target_post.id)
            return comment_group

        @pytest.fixture
        def parent_comment(self, target_comment_group):
            comment = CommentFactory(comment_group_id=target_comment_group.id)
            return comment

        @pytest.fixture
        def comment_obj(self, parent_comment):
            comment = CommentFactory.build(parent_id=parent_comment.id)
            return comment

        @pytest.fixture
        def subject(self, target_comment_group, comment_obj, user):
            resp = self.client.post('/comment_groups/%d/comments' % target_comment_group.id, data=layer_comment_create_form.dump(comment_obj).data)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_comment가_db에_저장된다(self, comment_obj, json_result):
            new_comment = Comment.query.get(json_result['id'])
            assert new_comment.content == comment_obj.content
            assert new_comment.step > 0

        class Context_target_comment_group이_없을_때:
            @pytest.fixture
            def subject(self, target_comment_group, comment_obj, user):
                wrong_id = target_comment_group.id + 123
                resp = self.client.post('/comment_groups/%d/comments' % wrong_id, data=layer_comment_create_form.dump(comment_obj).data)
                return resp

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

        class Context_parent_comment가_없을_때:
            @pytest.fixture
            def comment_obj(self, parent_comment):
                wrong_id = parent_comment.id + 123
                comment = CommentFactory.build(parent_id=wrong_id)
                return comment

            def test_404를_반환한다(self, subject):
                assert 404 == subject.status_code

    class Describe_delete_comment:
        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        # 댓글이 삭제되면 본인에 의해 삭제된 댓글임을 표시한다
        # 삭 제하면 댓글의 상태가 변경된다.
        @pytest.fixture
        def target_post(self):
            post = PostFactory()
            return post

        @pytest.fixture
        def target_group(self, target_post):
            group = CommentGroupFactory(post_id=target_post.id)
            return group

        @pytest.fixture
        def target_comment(self, target_group, user):
            comment = CommentFactory(comment_group_id=target_group.id, user_id=user.id, user=user)
            return comment

        @pytest.fixture
        def subject(self, target_comment, user):
            resp = self.client.delete('/comments/%d' % target_comment.id)
            return resp

        def test_204를_반환한다(self, subject):
            assert 204 == subject.status_code

        def test_해당_댓글의_상태가_변경된다(self, target_comment, subject):
            deleted_comment = Comment.query.get(target_comment.id)
            assert deleted_comment.is_deleted

        class Context_본인의_댓글이_아닐_때:
            @pytest.fixture
            def target_comment(self, target_group, user):
                wrong_user = UserFactory()
                comment = CommentFactory(comment_group_id=target_group.id, user_id=wrong_user.id, user=wrong_user)
                return comment

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code

    class Describe_update_comment:
        @pytest.fixture
        def user(self, logged_in_user):
            return logged_in_user

        @pytest.fixture
        def target_post(self):
            post = PostFactory()
            return post

        @pytest.fixture
        def target_group(self, target_post):
            group = CommentGroupFactory(post_id=target_post.id)
            return group

        @pytest.fixture
        def target_comment(self, target_group, user):
            comment = CommentFactory(comment_group_id=target_group.id, user_id=user.id, user=user)
            return comment

        @pytest.fixture
        def update_data(self):
            return dict(content='this is changed content')

        @pytest.fixture
        def subject(self, target_comment, update_data):
            print(update_data)
            resp = self.client.patch('/comments/%d' % target_comment.id, data=update_data)
            return resp

        def test_200을_반환한다(self, subject):
            assert 200 == subject.status_code

        def test_comment_content가_갱신된다(self, json_result):
            updated_comment = Comment.query.get(json_result['id'])
            assert updated_comment.content == 'this is changed content'

        @pytest.mark.parametrize('content', ['', None])
        class Context_content가_없을_때:
            @pytest.fixture
            def update_data(self, content):
                return dict(content=None)

            def test_422를_반환_한다(self, subject):
                assert 422 == subject.status_code

        @pytest.mark.parametrize('content', ['짧은 댓글', '10글자 이하', '메롱메롱'])
        class Context_content가_짧을_때:
            @pytest.fixture
            def update_data(self, content):
                return dict(content=content)

            def test_422를_반환_한다(self, subject):
                assert 422 == subject.status_code

        class Context_본인의_댓글이_아닐_때:
            @pytest.fixture
            def target_comment(self, target_group, user):
                wrong_user = UserFactory()
                comment = CommentFactory(comment_group_id=target_group.id, user_id=wrong_user.id, user=wrong_user)
                return comment

            def test_401을_반환한다(self, subject):
                assert 401 == subject.status_code



    # class Describe_create:
    #     @pytest.fixture
    #     def form(self):
    #         comment = FakeCommentFactory.build()
    #         return comment
    #
    #     @pytest.fixture
    #     def subject(self, target_post_id, form, user):
    #         resp = self.client.post('/posts/%d/comments' % target_post_id, data=comment_create_form_schema.dumps(form).data, content_type='application/json')
    #         return resp
    #
    #     def test_200을_반환한다(self, subject):
    #         assert 200 == subject.status_code
    #
    #     def test_DB에_comment가_저장된다(self, json_result, form, user):
    #         comment_id = json_result['id']
    #         db_comment = Comment.query.get(comment_id)
    #         assert db_comment.content == form.content
    #         assert db_comment.user_id == user.id
    #
    #     def test_post의_comment_count가_증가한다(self, json_result):
    #         db_comment = Comment.query.get(json_result['id'])
    #         assert 1 == db_comment.post.comment_count
    #
    #     class Context_로그인을_하지_않았을_때:
    #         @pytest.fixture
    #         def user(self, not_logged_in_user):
    #             return not_logged_in_user
    #
    #         def test_401을_반환한다(self, subject):
    #             assert 401 == subject.status_code
    #
    #     class Context_content가_없을_때:
    #         @pytest.fixture
    #         def form(self):
    #             comment = FakeCommentFactory.build(content='')
    #             return comment
    #
    #         def test_422를_반환한다(self, subject):
    #             assert 422 == subject.status_code
    #
    #     class Context_post가_없을_때:
    #         @pytest.fixture
    #         def target_post_id(self):
    #             post = FakePostFactory.build()
    #             return post.id
    #
    #         def test_404를_반환한다(self, subject):
    #             assert 404 == subject.status_code
    #
    # class Describe_delete:
    #     @pytest.fixture
    #     def target_comment_id(self, user):
    #         comment = FakeCommentFactory(user=user, user_id=user.id)
    #         comment.post.comment_count = 1
    #         self.session.commit()
    #         return comment.id
    #
    #     @pytest.fixture
    #     def subject(self, target_comment_id):
    #         resp = self.client.delete('/comments/%d' % target_comment_id)
    #         return resp
    #
    #     def test_204를_반환한다(self, subject):
    #         assert 204 == subject.status_code
    #
    #     def test_DB의_comment가_삭제된다(self, subject, target_comment_id):
    #         db_comment = Comment.query.get(target_comment_id)
    #         assert db_comment.is_deleted
    #
    #     def test_post의_comment_count가_감소한다(self, subject, target_comment_id):
    #         db_comment = Comment.query.get(target_comment_id)
    #         assert 0 == db_comment.post.comment_count
    #
    #     class Context_comment가_존재하지_않을_때:
    #         @pytest.fixture
    #         def target_comment_id(self, user):
    #             comment = FakeCommentFactory.build(user=user, user_id=user.id)
    #             return comment.id
    #
    #         def test_404를_반환한다(self, subject):
    #             assert 404 == subject.status_code
    #
    #     class Context_로그인_하지_않았을_때:
    #         @pytest.fixture
    #         def user(self, not_logged_in_user):
    #             return not_logged_in_user
    #
    #         def test_401를_반환한다(self, subject):
    #             assert 401 == subject.status_code
    #
    #     class Context_본인_게시글이_아닌_경우:
    #         @pytest.fixture
    #         def target_comment_id(self):
    #             comment = FakeCommentFactory()
    #             return comment.id
    #
    #         def test_401를_반환한다(self, subject):
    #             assert 401 == subject.status_code
    #
    # class Describe_update:
    #     @pytest.fixture
    #     def update_data(self):
    #         return dict(content='changed content.')
    #
    #     @pytest.fixture
    #     def target_comment(self, user):
    #         target_comment = FakeCommentFactory(user=user, user_id=user.id)
    #         self.session.commit()
    #         return target_comment
    #
    #     @pytest.fixture
    #     def subject(self, update_data, target_comment):
    #         resp = self.client.patch('/comments/%d' % target_comment.id, data=comment_update_form_schema.dumps(update_data).data, content_type='application/json')
    #         return resp
    #
    #     def test_200을_반환한다(self, subject):
    #         assert 200 == subject.status_code
    #
    #     def test_DB의_comment값이_갱신된다(self, json_result):
    #         db_comment = Comment.query.get(json_result['id'])
    #
    #         assert db_comment.content == 'changed content.'
    #
    #     class Context_본인의_게시글이_아닌_경우:
    #         @pytest.fixture
    #         def target_comment(self):
    #             comment = FakeCommentFactory()
    #             self.session.commit()
    #             return comment
    #
    #         def test_401을_반환한다(self, subject):
    #             assert 401 == subject.status_code
    #
    #     class Context_로그인_하지_않았을_때:
    #         @pytest.fixture
    #         def user(self, not_logged_in_user):
    #             return not_logged_in_user
    #
    #         def test_401을_반환한다(self, subject):
    #             assert 401 == subject.status_code
    #
    #     @pytest.mark.parametrize('content', ['', None])
    #     class Context_content가_존재하지_않을_때:
    #         @pytest.fixture
    #         def update_data(self, content):
    #             return dict(content=content)
    #
    #         def test_422를_반환한다(self, subject):
    #             assert 422 == subject.status_code
    #
    #     class Context_comment가_존재하지_않을_때:
    #         @pytest.fixture
    #         def target_comment(self, user):
    #             comment = FakeCommentFactory.build(user=user, user_id=user.id)
    #             return comment
    #
    #         def test_404를_반환한다(self, subject):
    #             assert 404 == subject.status_code
    #





