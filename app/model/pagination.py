
class Pagination(object):
    def __init__(self, per_page, page, has_prev, has_next):
        self.per_page = per_page
        self.page = page
        self.has_prev = has_prev
        self.has_next = has_next

    def __repr__(self):
        return '<Pagination per_page: %d, page: %d>' % (self.per_page, self.page)
