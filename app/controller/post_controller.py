from flask import Blueprint, abort, request
from webargs.flaskparser import use_args
from app.service import post_service
from app.model.post import Post
from app.schema.post import post_schema, simple_posts_schema
from app.schema.resp import resp_schema
from flask_login import login_required, current_user



bp = Blueprint('post', __name__)


'''
글
목록, 생성, 삭제, 수정, 읽기
'''


# list post
# GET /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['GET'])
@login_required
def post_view(bid):
    posts = Post.query.filter(Post.board_id==bid).filter(Post.status!=2).order_by(Post.created_at.desc()).paginate(per_page=3, error_out=False)
    posts.page = int(request.args.get('page')) if request.args.get('page') else 1

    result = dict(data=simple_posts_schema.dump(posts.items).data, status_code=200)

    return resp_schema.jsonify(result), 200


# read post
# GET /posts/1
@bp.route('/posts/<int:pid>', methods=['GET'])
@login_required
def detail_view(pid):
    result = post_service.read(pid)

    return resp_schema.jsonify(result), result['status_code']


# create post
# POST /boards/1/posts
@bp.route('/boards/<int:bid>/posts', methods=['POST'])
@login_required
@use_args(post_schema)
def create(post_args, bid):
    try:
        result = post_service.create(bid, post_args, current_user)
        return resp_schema.jsonify(result), 200
    except Exception as e:
        return 'Server Error.', 500


# update post
# PATCH /posts/1
@bp.route('/posts/<int:pid>', methods=['PATCH'])
@login_required
@use_args(post_schema)
def update(post_args, pid):
    result = post_service.update(pid, post_args)

    return resp_schema.jsonify(result), result['status_code']


# delete post
# DELETE /posts/1
@bp.route('/posts/<int:pid>', methods=['DELETE'])
@login_required
def delete(pid):
    result = post_service.delete(pid)

    return resp_schema.jsonify(result), result['status_code']