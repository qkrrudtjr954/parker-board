from parker_board.schema import ma
from marshmallow import fields


class RespSchema(ma.Schema):
    data = fields.Dict(missing=None)
    errors = fields.Dict(missing=None)
    status_code = fields.Integer(missing=500)


resp_schema = RespSchema()


