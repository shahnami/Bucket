import json
from ..page import Page


class Collection:
    """ Abstract Collection Class """

    def __init__(self):
        self.check: dict = {'domain': True, 'element': True}
        self.keywords: [any] = list()
        self.pages: [Page] = list()

    def __dict__(self):
        return {
            f"{self.__class__.__name__}": {
                "check": self.check,
                "keywords": self.keywords,
                "page_count": len(self.pages),
                "pages": [{"domain": page.domain, "matched_on": page.matched} for page in self.pages]
            }
        }

    def pretty_print(self):
        print(f"Found {len(self.pages)} pages in {self.__class__.__name__}")
        for page in self.pages:
            print(json.dumps({page.domain: page.matched}, indent=4))

    def validate(self, *, page: Page):
        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], element=self.check['element']):
                page.add_match(keyword)
                self.pages.append(page)
                self.pages = list(set(self.pages))
