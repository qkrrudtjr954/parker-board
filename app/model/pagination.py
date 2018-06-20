
class Pagination(object):
    def __init__(self, per_page, page, pages, has_prev, has_next):
        self.per_page = per_page
        self.page = page
        self.pages = pages
        self.has_prev = has_prev
        self.has_next = has_next

    def __repr__(self):
        return '<Pagination pages: %d, per_page: %d, page: %d>' % (self.pages, self.per_page, self.page)
