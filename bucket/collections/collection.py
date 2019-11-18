import json
from ..page import Page


class Collection:
    """ Abstract Collection Class """

    def __init__(self):
        self.name: str = 'Abstract Collection'
        self.check: dict = {'domain': True, 'element': True}
        self.keywords: [any] = list()
        self.pages: [Page] = list()

    def __dict__(self) -> dict:
        return {
            f"{self.name}": {
                "check": self.check,
                "keywords": self.keywords,
                "page_count": len(self.pages),
                "pages": [{"domain": page.domain, "ip": [str(ip) for ip in page.ip], "matched_on": [matched for matched in page.matched if matched in self.keywords]} for page in self.pages]
            }
        }

    def validate(self, *, page: Page):
        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], element=self.check['element']):
                page.add_match(keyword)
                self.pages.append(page)
                self.pages = list(set(self.pages))
