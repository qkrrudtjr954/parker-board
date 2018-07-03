
class Pagination(object):
    def __init__(self, per_page, page):
        self.per_page = per_page
        self.page = page

    def __repr__(self):
        return '<Pagination per_page: %d, page: %d>' % (self.per_page, self.page)
