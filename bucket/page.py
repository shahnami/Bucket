from netaddr import IPAddress, IPNetwork
from bs4 import BeautifulSoup
import dns.resolver


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
        self.ssl: dict = ssl            # {"ssl": bool, "valid": bool}
        self.fetch_title()

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
        self.ip = dns_records

    def __repr__(self):
        return f"{self.domain}"

    def __str__(self):
        return f"{self.domain},{self.content}"
