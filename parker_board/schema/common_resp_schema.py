from marshmallow import fields
from parker_board.schema import ma


class CommonRespSchema(ma.Schema):
    status_code = fields.Integer()
    message = fields.String()


common_resp_schema = CommonRespSchema()