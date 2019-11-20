import json
from ..page import Page


class Collection:
    """ Abstract Collection Class """

    def __init__(self):
        self.name: str = 'Abstract Collection'
        self.check: dict = {'domain': True, 'content': True, 'status': False}
        self.keywords: [any] = list()
        self.pages: [Page] = list()

    def __dict__(self) -> dict:
        return {
            f"{self.name}": {
                "check": self.check,
                "keywords": self.keywords,
                "page_count": len(self.pages),
                "pages": [{"domain": page.domain, "ip": [str(ip) for ip in page.ip], "matched_on": [matched for matched in page.matched if matched in self.keywords], "status": page.status, "server": page.header, "redirect": page.redirect, "title": page.title, "is_dupe": page.is_dupe} for page in self.pages]
            }
        }

    def dedupe(self, *, page: Page):
        # TODO: Use Levenshtein Distance on page.content instead
        if not page.sitemap_hash == '-':
            for p in self.pages:
                if not p.domain == page.domain:
                    if page.sitemap_hash == p.sitemap_hash and page.header == p.header:
                        page.set_dupe(is_dupe=True)

    def validate(self, *, page: Page):
        for keyword in self.keywords:
            if keyword in page.check_in(domain=self.check['domain'], content=self.check['content'], status=self.check['status']):
                page.add_match(keyword=keyword)
                self.pages.append(page)
                self.pages = list(set(self.pages))
