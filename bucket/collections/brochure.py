from .collection import Collection
from ..page import Page


class BrochureCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name = 'Brochure Collection'
        self.pages = list()
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form', 'contact', 'logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email', 'vpn', 'ssl']

    def validate(self, *, page: Page):
        contains_keywords = False
        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], content=self.check['content'], status=self.check['status']):
                contains_keywords = True

        if not contains_keywords:
            self.pages.append(page)
            self.pages = list(set(self.pages))
