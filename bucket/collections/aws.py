from netaddr import IPNetwork
from .collection import Collection
from ..page import Page


class AWSCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.pages = list()
        self.check = {'domain': False, 'element': False}
        self.keywords = list()

    def __dict__(self):
        return {
            f"{self.__class__.__name__}": {
                "check": self.check,
                "page_count": len(self.pages),
                "pages": [{"domain": page.domain, "matched_on": page.matched} for page in self.pages]
            }
        }

    def set_keywords(self, *, ranges: [IPNetwork]):
        self.keywords = ranges

    def validate(self, *, page: Page):
        for keyword in self.keywords:
            for ip in page.ip:
                if ip in keyword:
                    page.add_match(ip.format())
                    self.pages.append(page)
                    self.pages = list(set(self.pages))
