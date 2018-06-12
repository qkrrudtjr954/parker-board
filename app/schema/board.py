from app.model import db
from app.model.board import Board, BoardStatus
from app.schema import ma
from app.schema.user import simple_user_schema

from marshmallow import fields
from marshmallow_enum import EnumField

'''
스키마는 입력값 정제 vs 나가는값 정제

입력값 정제 : 필요한 스키마 만들어서 사용
출력값 정제 : 기본 스키마에서 only를 사용
'''


class BoardSchema(ma.ModelSchema):
    status = EnumField(BoardStatus)
    user = fields.Nested(simple_user_schema)    # simple_user_schema 는 user의 id, email 필드만 갖는다.

    class Meta:
        strict = True
        model = Board
        sqla_session = db.session


main_board_schema = BoardSchema(only=['id', 'title', 'description', 'created_at', 'user'], many=True)
simple_board_schema = BoardSchema(only=['id', 'title', 'description'])


# fixme: 테스트코드 때문에 스키마가 바뀌면 안됨.
after_delete_board_schema = BoardSchema(only=['id', 'title', 'status'])
after_update_board_schema = BoardSchema(only=['id', 'title', 'description', 'status', 'updated_at'])
after_create_board_schema = BoardSchema(only=['id', 'title', 'description', 'status', 'updated_at', 'user'])


# Board를 생성하거나 수정할 때 사용하는 스키마
class BoardFormSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Board
        sqla_session = db.session
        fields = ['title', 'description']


board_create_form_schema = BoardFormSchema()
board_update_form_schema = BoardFormSchema()

