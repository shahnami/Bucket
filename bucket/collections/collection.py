import json
import operator
from ..config import WEIGHTS
from ..page import Page


class Collection:
    """ Abstract Collection Class """

    def __init__(self):
        self.name: str = 'Abstract Collection'
        self.check: dict = {'domain': True, 'content': True, 'status': False}
        self.keywords: [any] = list()
        #{"www.example.com": str: {"page": Page, "matched": list}, ...}
        self.pages: dict = dict()
        self.weight: int = 1

    def set_weight(self):
        if(self.name in WEIGHTS):
            self.weight = WEIGHTS[self.name]
        else:
            self.weight = 1

    def __dict__(self) -> dict:
        return {
            f"{self.name}": {
                "check": self.check,
                "keywords": self.keywords,
                "page_count": len(self.pages),
                "pages": [{"domain": page['page'].domain, "ip": [str(ip) for ip in page['page'].ip], "matched_on": [matched for matched in page['matched'] if matched in self.keywords], "status": page['page'].status, "server": page['page'].header, "redirect": page['page'].redirect, "title": page['page'].title} for domain, page in self.pages.items()]
            }
        }

    def dedupe(self, *, page: Page):
        # TODO: Use Levenshtein Distance on page.content instead
        if not page.sitemap_hash == '-':
            for key, value in self.pages.items():
                if value['page'].domain is not page.domain:
                    if page.sitemap_hash == value['page'].sitemap_hash and page.header == value['page'].header:
                        page.set_dupe(is_dupe=True)

    def validate(self, *, page: Page):
        entry: dict = {"page": page, "matched": list()}

        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], content=self.check['content'], status=self.check['status']):
                entry['matched'].append(keyword)
                entry['matched'] = list(set(entry['matched']))

        if entry['matched']:
            self.pages[page.domain] = entry

    def get_page(self, *, page: Page) -> dict:
        if page.domain in self.pages:
            return self.pages[page.domain]
        return None

    @classmethod
    def get_highest_score(cls, *, page: Page, collections: list):
        winner: Collection = None
        stats: dict = dict()

        for collection in collections:
            collection_page = collection.get_page(page=page)
            if collection_page:
                stats[collection] = collection.weight <= 1 and len(collection_page['matched']) or collection.weight
            if(stats):
                winner = max(stats, key=stats.get)
        return winner
