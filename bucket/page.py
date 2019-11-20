from netaddr import IPAddress, IPNetwork
import dns.resolver


class Page:
    """ DOM element of a web apge """

    def __init__(self, *, domain: str, status: int, redirected: str, header: str, element: str):
        self.domain: str = domain
        self.redirected: str = redirected
        self.status: int = status
        self.header: str = header
        self.element: str = element
        self.matched: [any] = []
        self.ip: [IPAddress] = []

    def add_match(self, keyword: str):
        if(keyword not in self.matched):
            self.matched.append(keyword)

    def check_in(self, *, domain: bool, element: bool, status: bool) -> str:
        if(domain and element and status):
            return f"{self.domain},{self.element},{self.element}"
        elif(domain and element):
            return f"{self.domain},{self.element}"
        elif(domain and status):
            return f"{self.domain},{self.status}"
        elif(element and status):
            return f"{self.element},{self.status}"
        elif(domain):
            return f"{self.domain}"
        elif(element):
            return f"{self.element}"
        elif(status):
            return f"{self.status}"
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
        return f"{self.domain},{self.element}"
