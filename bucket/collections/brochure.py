from .collection import Collection
from ..page import Page


class BrochureCollection(Collection):
    """ Brochure Collection class 

        Sites which contain static content, brochureware.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'Brochure Collection'
        self.check = {'domain': True, 'content': True, 'status': False}
        self.keywords = ['input', 'form', 'contact', 'logon', 'signup', 'signin', 'login',
                         'register', 'auth', 'passw', 'username', 'email', 'vpn', 'ssl']
        self.set_weight()

    def validate(self, *, page: Page):
        entry: dict = {"page": page, "matched": list()}

        contains_keywords = False
        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], content=self.check['content'], status=self.check['status']):
                contains_keywords = True

        if not contains_keywords:
            self.pages[page.domain] = entry
