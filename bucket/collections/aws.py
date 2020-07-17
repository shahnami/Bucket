from netaddr import IPAddress, IPNetwork
from .collection import Collection
from ..page import Page


class AWSCollection(Collection):
    """ AWS Collection class 

        Sites for which the A-records match the AWS public IP range.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'AWS Collection'
        self.check = {'domain': False, 'content': False, 'status': False}
        self.set_weight()

    def __dict__(self) -> dict:
        return {
            f"{self.name}": {
                "check": self.check,
                "page_count": len(self.pages),
                "pages": [{"domain": page['page'].domain, "ip": [str(ip) for ip in page['page'].ip], "matched_on": self.get_match_for(partial_page=page)} for domain, page in self.pages.items()]
            }
        }

    def get_match_for(self, *, partial_page: dict) -> list:
        matches = list()

        for match in partial_page['matched']:
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
        entry: dict = {"page": page, "matched": list()}

        for keyword in self.keywords:
            for ip in page.ip:
                if ip in keyword:
                    entry['matched'].append(ip.format())
                    entry['matched'] = list(set(entry['matched']))
        if entry['matched']:
            self.pages[page.domain] = entry
