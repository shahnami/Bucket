import json
import urllib3
import requests
import tldextract
import hashlib
import dns.resolver
from netaddr.ip import IPAddress, IPNetwork

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 2

AWS_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


# Work on this function:

# cat /tmp/domains | while read domain; do curl "https://domain-availability-api.whoisxmlapi.com/api/v1?domainName=$domain&outputFormat=JSON&mode=DNS_AND_WHOIS" -H 'Accept: text/html, */*; q=0.01' -H 'Referer: https://domain-availability-api.whoisxmlapi.com/' -H 'Sec-Fetch-Dest: empty' -H 'X-CSRF-TOKEN: 5ZezD0JXpWysb1paZgCSiPu2xVCAcGyP2PjbW67T' -H 'X-Requested-With: XMLHttpRequest' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36' -H 'DNT: 1' --compressed ; sleep 1; echo; done


def is_available(*, domain: str) -> bool:

    return False


def get_sitemap_hash(*, domain: str) -> str:
    try:
        ext = tldextract.extract(domain)
        request = requests.get(
            f"https://{ext.registered_domain}/sitemap.xml", verify=False, allow_redirects=False, timeout=10)

        hash = hashlib.sha256(request.content).hexdigest()
        return hash
    except:
        return "-"


def is_redirect_in_scope(*, domains: list, location: str) -> bool:
    redirect_domain = tldextract.extract(location)
    for domain in domains:
        ext = tldextract.extract(domain)
        if redirect_domain.registered_domain == ext.registered_domain:
            return True
    return False


def get_aws_ranges(*, url: str = AWS_URL) -> list:
    print(f"[-] Fetching AWS ranges {url}")
    aws_ranges = list()
    aws = list()

    with requests.get(url) as req:
        aws_ranges = json.loads(req.content.decode())

    for prefix in aws_ranges['prefixes']:
        aws.append(IPNetwork(prefix['ip_prefix']))
    return aws


def fetch_dom(*, domains: list, domain: str, get_source: bool, output_path: str) -> dict:
    """ Fetch DOM element for domain """

    try:
        new_domain = domain
        smhash = '-'
        header = '-'
        redirect = {"location": "-", "in_scope": False}
        ssl = {"ssl": False, "valid": False}
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-gb",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
        }

        if 'http' not in domain:
            new_domain = f"https://{domain}"

        try:
            try:
                request = requests.get(
                    new_domain, verify=True, allow_redirects=True, timeout=10, headers=headers)
                ssl['ssl'] = True
                ssl['valid'] = True
            except:
                request = requests.get(
                    new_domain, verify=False, allow_redirects=True, timeout=10, headers=headers)
                ssl['ssl'] = True
                ssl['valid'] = False
        except:
            try:
                new_domain = f"http://{domain}"
                request = requests.get(
                    new_domain, verify=False, allow_redirects=True, timeout=10, headers=headers)
            except:
                print(f"[x] Error connecting to: {domain}")
                return {
                    "domain": domain,
                    "status": -1,
                    "header": header,
                    "smhash": smhash,
                    "redirect": redirect,
                    "ssl": ssl,
                    "content": 'error-connecting'
                }

        # Fetch sitemap.xml for dupe checking
        if(len(request.history) > 1):
            smhash = get_sitemap_hash(domain=request.history[-1].url)
        else:
            smhash = get_sitemap_hash(domain=new_domain)

            # Check if headers have 'Server' information
        if 'Server' in request.headers:
            header = request.headers['Server']

        # Check if request is redirected
        if(len(request.history) > 1):
            # TODO: What if there are multiple redirects?
            old_headers = request.history[0].headers
            if 'Location' in old_headers:
                redirect["location"] = old_headers['Location']
                redirect["in_scope"] = is_redirect_in_scope(
                    domains=domains, location=old_headers['Location'])

                # TODO:
                # Check if location starts with '/...' - some outliers have a local redirect
                # Check how subdomains react to this?
                # if not is_redirect_in_scope(location=old_headers['Location']):
                if not ("//"+domain in old_headers['Location'] or "//www"+domain in old_headers['Location']):
                    return {
                        "domain": domain,
                        "status": request.history[0].status_code,
                        "header": header,
                        "smhash": smhash,
                        "redirect": redirect,
                        "ssl": ssl,
                        "content": 'out-of-scope, 3xx-redirect-response'
                    }

        page: dict = {
            "domain": domain,
            "status": request.status_code,
            "header": header,
            "smhash": smhash,
            "redirect": redirect,
            "ssl": ssl,
            "content": '-'
        }

        if(request.status_code >= 200 and request.status_code < 300):
            if(get_source):
                with open(f"{output_path}{domain.replace('/', '').replace(':', '')}.txt", 'w') as file:
                    file.writelines(
                        request.content.decode('utf-8').lower())
            page['content'] = request.content.decode().lower()
        elif(request.status_code >= 300 and request.status_code < 400):
            page['content'] = '3xx-redirect-response'
        elif(request.status_code == 401):
            page['content'] = 'login, 4xx-client-response'
        elif(request.status_code == 402):
            page['content'] = 'payment, 4xx-client-response'
        elif(request.status_code == 404):
            page['content'] = '404-page-not-found'
        elif(request.status_code >= 400 and request.status_code < 500):
            page['content'] = '4xx-client-response'
        elif(request.status_code >= 500):
            page['content'] = '5xx-server-response'
        else:
            print(
                f"[x] {domain} returned status code: {request.status_code}")
            page['content'] = 'unhandled-status-code'

    except Exception as e:
        print(f"[x] {domain} returned error: {e}")
        page['content'] = 'exception-thrown'
        page['status'] = -1

    return page
