from netaddr import IPAddress, IPNetwork
from bs4 import BeautifulSoup
import dns.resolver

from .utils import fetch_dom


class Page:
    """ Web Page Class """

    def __init__(self, *, domain: str, status: int, redirect: dict = dict(), header: str = '-', content: str = 'exception-thrown', smhash: str = '-', ssl: dict = {"ssl": False, "valid": False}):
        self.domain: str = domain
        self.redirect: dict = redirect  # {"location": str, "in_scope": bool}
        self.status: int = status
        self.header: str = header
        self.content: str = content
        self.title: str = '-'
        self.is_dupe: bool = False
        self.sitemap_hash: str = smhash
        self.ip: [IPAddress] = list()
        self.dns_records: dict = dict()
        self.ssl: dict = ssl            # {"ssl": bool, "valid": bool}
        self.related_pages: [Page] = list()
        self.fetch_title()

    def sanitize_url(self, *,  url: str) -> str:
        if 'javascript:' in url.lower():
            return None
        elif url.startswith(self.domain) or url.startswith('http') or url.startswith('www.'):
            return url
        elif url.startswith('/') or len(url) == 1:
            return f"{self.domain}{url}"
        else:
            return f"{self.domain}/{url}"

    def get_links(self) -> list:
        soup = BeautifulSoup(self.content, 'html.parser')

        related_links: list = list()
        for link in soup.find_all('a', href=True):
            sanitized = self.sanitize_url(url=link['href'])
            if sanitized:
                related_links.append(sanitized)

        for link in soup.find_all('img', src=True):
            sanitized = self.sanitize_url(url=link['src'])
            if sanitized:
                related_links.append(sanitized)

        for link in soup.find_all('script', src=True):
            sanitized = self.sanitize_url(url=link['src'])
            if sanitized:
                related_links.append(sanitized)

        return related_links

    def fetch_related_pages(self, *, resolve_dns: bool, domains: list, get_source: bool, output_path: str):
        for link in self.get_links():
            page_dom = fetch_dom(domains=domains, domain=link,
                                 get_source=get_source, output_path=output_path)
            page = Page.page_from(page=page_dom)
            if page:
                if resolve_dns:
                    page.set_domain_dns()
                self.related_pages.append(page)

    def fetch_title(self):
        try:
            soup = BeautifulSoup(self.content, 'html.parser')
            if(soup.title.string):
                self.title = soup.title.string.strip()
            else:
                self.title = '-'
        except:
            self.title = '-'

    def set_dupe(self, *, is_dupe: bool):
        self.is_dupe = is_dupe

    def check_in(self, *, domain: bool, content: bool, status: bool) -> str:
        if(domain and content and status):
            return f"{self.domain},{self.content},{self.status}".lower()
        elif(domain and content):
            return f"{self.domain},{self.content}".lower()
        elif(domain and status):
            return f"{self.domain},{self.status}".lower()
        elif(content and status):
            return f"{self.content},{self.status}".lower()
        elif(domain):
            return f"{self.domain}".lower()
        elif(content):
            return f"{self.content}".lower()
        elif(status):
            return f"{self.status}".lower()
        else:
            return f"-"

    def set_dns_txt_records(self) -> list:
        """ Fetch DNS TXT records for domain"""

        txt_records = list()

        try:
            for record in dns.resolver.query(self.domain, "TXT").response.answer[0]:
                txt_records.append(str(record))
        except:
            self.dns_records['txt'] = []

        self.dns_records['txt'] = txt_records

    def set_domain_dns(self) -> [IPAddress]:
        """Get the DNS record, if any, for the given domain."""
        dns_records = list()
        try:
            # get the dns resolutions for this domain
            dns_results = dns.resolver.query(self.domain)
            dns_records = [IPAddress(ip.address) for ip in dns_results]
        except dns.resolver.NXDOMAIN:
            # the domain does not exist so dns resolutions remain empty
            pass
        except dns.resolver.NoAnswer:
            # the resolver is not answering so dns resolutions remain empty
            pass
        except dns.resolver.NoNameservers:
            pass
        except dns.resolver.Timeout:
            pass
        except:
            pass
        self.ip = dns_records

    def __repr__(self):
        return f"{self.domain}"

    def __str__(self):
        return f"{self.domain},{self.content}"

    @classmethod
    def page_from(cls, *, page: dict):
        return Page(domain=page['domain'], status=page['status'], header=page['header'], smhash=page['smhash'], redirect=page['redirect'], ssl=page['ssl'], content=page['content'])
