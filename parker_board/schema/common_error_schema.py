from marshmallow import fields
from parker_board.schema import ma


class CommonErrorSchema(ma.Schema):
    status_code = fields.Integer()
    errors = fields.String()


common_error_schema = CommonErrorSchema()