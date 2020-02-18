from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils import fetch_dom
from .page import Page


class Bucketer:
    """ Main Bucketing Class """

    def __init__(self, *, configuration: dict = {"input_path": "targets.txt",
                                                 "collections": [],
                                                 "get_source": True,
                                                 "resolve_dns": True,
                                                 "is_recursive": False,
                                                 "output_path": "/tmp/"}):
        self._configuration = configuration
        self._domains: list = list()
        self._collections: list = list()
        self._pages: list = list()

    def get_page_for(self, *, domain: str) -> Page:
        page_dom: dict = fetch_dom(domains=self.get_domains(
        ), domain=domain, get_source=self._configuration['get_source'], output_path=self._configuration['output_path'])
        page = Page.page_from(page=page_dom)
        if page:
            if self._configuration['is_recursive']:
                page.fetch_related_pages(resolve_dns=self._configuration['resolve_dns'], domains=self.get_domains(
                ), get_source=self._configuration['get_source'], output_path=self._configuration['output_path'])
            if self._configuration['resolve_dns']:
                page.set_domain_dns()
            return page
        return None

    def run(self):
        print(f"[-] Reading {self._configuration['input_path']}")

        if self._configuration['get_source']:
            print(
                f"[-] Downloading Page Source in: {self._configuration['output_path']}")

        with open(self._configuration['input_path']) as targets:
            domains = [target.strip() for target in targets.readlines()]

        with ThreadPoolExecutor(max_workers=50) as exc:
            pages = list(
                exc.map(lambda domain: self.get_page_for(domain=domain), domains))

        for collection in self._configuration['collections']:
            for page in pages:
                collection.validate(page=page)
                # TODO: Dedupe needs extra sanity checking
                # collection.dedupe(page=page)

        if self._configuration['get_source']:
            print(f"[*] Page Sources: {self._configuration['output_path']}")

        self.set_domains(domains=domains)
        self.set_pages(pages=pages)
        self.set_collection(collection=self._configuration['collections'])

    # Class Setters and Getters

    def set_domains(self, *, domains: list):
        self._domains = domains

    def set_pages(self, *, pages: list):
        self._pages = pages

    def set_collection(self, *, collection: list):
        self._collections = collection

    def get_domains(self) -> list:
        return self._domains

    def get_pages(self) -> list:
        return self._pages

    def get_collections(self) -> list:
        return self._collections
