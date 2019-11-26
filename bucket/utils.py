#!/bin/python3

import json
import urllib3
import requests
import tldextract
import hashlib
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr.ip import IPAddress, IPNetwork
from .page import Page

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 2

AWS_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
ALL_DOMAINS = list()


def fetch_dom(*, domain: str, get_source: bool, output_path: str) -> Page:
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
                return Page(domain=domain, status=-1, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='error-connecting')

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
                    location=old_headers['Location'])

                # TODO:
                # Check if location starts with '/...' - some outliers have a local redirect
                # Check how subdomains react to this?
                # if not is_redirect_in_scope(location=old_headers['Location']):
                if not ("//"+domain in old_headers['Location'] or "//www"+domain in old_headers['Location']):
                    return Page(domain=domain, status=request.history[0].status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='out-of-scope, 3xx-redirect-response')

        if(request.status_code >= 200 and request.status_code < 300):
            if(get_source):
                with open(f"{output_path}{domain.replace('/', '').replace(':', '')}.txt", 'w') as file:
                    file.writelines(request.content.decode('utf-8').lower())
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content=request.content.decode().lower(),)
        elif(request.status_code >= 300 and request.status_code < 400):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='3xx-redirect-response')
        elif(request.status_code == 401):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='login, 4xx-client-response')
        elif(request.status_code == 402):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='payment, 4xx-client-response')
        elif(request.status_code == 404):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='404-page-not-found')
        elif(request.status_code >= 400 and request.status_code < 500):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='4xx-client-response')
        elif(request.status_code >= 500):
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='5xx-server-response')
        else:
            print(f"[x] {domain} returned status code: {request.status_code}")
            return Page(domain=domain, status=request.status_code, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='unhandled-status-code')

    except Exception as e:
        print(f"[x] {domain} returned error: {e}")
        return Page(domain=domain, status=-1, header=header, smhash=smhash, redirect=redirect, ssl=ssl, content='exception-thrown')


def get_sitemap_hash(*, domain: str) -> str:
    try:
        ext = tldextract.extract(domain)
        request = requests.get(
            f"https://{ext.registered_domain}/sitemap.xml", verify=False, allow_redirects=False, timeout=10)

        hash = hashlib.sha256(request.content).hexdigest()
        return hash
    except:
        return "-"


def is_redirect_in_scope(*, location: str) -> bool:
    redirect_domain = tldextract.extract(location)
    for domain in ALL_DOMAINS:
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


def parse_domain(*, domain: str, get_source: bool, output_path: str) -> Page:
    page = fetch_dom(domain=domain, get_source=get_source,
                     output_path=output_path)

    if(page):
        page.set_domain_dns()
        return page
    return None


def process(*, input_path: str, collections: list, get_source: bool = True, output_path: str = '/tmp/') -> (list, list):
    print(f"[-] Reading {input_path}")

    if get_source:
        print(f"[-] Downloading Page Source in: {output_path}")

    with open(input_path) as targets:
        domains = [target.strip() for target in targets.readlines()]

    global ALL_DOMAINS
    ALL_DOMAINS = domains

    with ThreadPoolExecutor(max_workers=50) as exc:
        pages = list(exc.map(lambda domain: parse_domain(
            domain=domain, get_source=get_source, output_path=output_path), domains))

    for collection in collections:
        for page in pages:
            collection.validate(page=page)
            # TODO: Dedupe needs extra sanity checking
            # collection.dedupe(page=page)

    if get_source:
        print(f"[*] Page Sources: {output_path}")

    return collections, pages
