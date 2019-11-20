from netaddr import IPAddress, IPNetwork
from .collection import Collection
from ..page import Page


class AWSCollection(Collection):
    """ Collection class """

    def __init__(self):
        self.name: str = 'AWS Collection'
        self.pages = list()
        self.check = {'domain': False, 'element': False, 'status': False}
        self.keywords = list()

    def __dict__(self) -> dict:
        return {
            f"{self.name}": {
                "check": self.check,
                "page_count": len(self.pages),
                "pages": [{"domain": page.domain, "ip": [str(ip) for ip in page.ip], "matched_on": self.get_match_for(page=page)} for page in self.pages]
            }
        }

    def get_match_for(self, *, page: Page) -> list:
        matches = list()
        for match in page.matched:
            for keyword in self.keywords:
                try:
                    if IPAddress(match) in keyword:
                        matches.append(match)
                        break
                except:
                    pass
        return matches

    def set_keywords(self, *, ranges: [IPNetwork]):
        self.keywords = ranges

    def validate(self, *, page: Page):
        for keyword in self.keywords:
            for ip in page.ip:
                if ip in keyword:
                    page.add_match(ip.format())
                    self.pages.append(page)
                    self.pages = list(set(self.pages))
