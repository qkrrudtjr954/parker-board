from app.schema import ma
from marshmallow import fields, post_load
from app.model.pagination import Pagination


class PaginationSchema(ma.Schema):
    per_page = fields.Integer(missing=10)
    page = fields.Integer(missing=1)
    pages = fields.Integer(missing=1)
    has_next = fields.Boolean(missing=False, required=False)
    has_prev = fields.Boolean(missing=False, required=False)

    @post_load
    def make_pagination(self, data):
        return Pagination(**data)

    class Meta:
        strict = True


pagination_schema = PaginationSchema()
