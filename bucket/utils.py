#!/bin/python3

import json
import csv
import urllib3
import requests
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr.ip import IPAddress, IPNetwork
from .page import Page

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 2

AWS_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def fetch_dom(*, domain: str, get_source: bool, output_path: str) -> Page:
    """ Fetch DOM element for domain """
    # session = HTMLSession(verify=False)
    try:
        new_domain = domain
        header = '-'
        redirect_location = '-'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-gb",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
        }

        if 'http' not in domain:
            new_domain = f"https://{domain}"

        try:
            request = requests.get(
                new_domain, verify=False, allow_redirects=False, timeout=10, headers=headers)
        except:
            new_domain = f"http://{domain}"
            request = requests.get(
                new_domain, verify=False, allow_redirects=False, timeout=10, headers=headers)

        if 'Server' in request.headers:
            header = request.headers['Server']

        if 'Location' in request.headers:
            redirect_location = request.headers['Location']

        if(request.status_code >= 200 and request.status_code < 300):
            if(get_source):
                with open(f"{output_path}{domain.replace('/', '').replace(':', '')}.txt", 'w') as file:
                    file.writelines(request.content.decode().lower())
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element=request.content.decode().lower())
        elif(request.status_code >= 300 and request.status_code < 400):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='3xx-redirect-response')
        elif(request.status_code == 401):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='login, 4xx-client-response')
        elif(request.status_code == 402):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='payment, 4xx-client-response')
        elif(request.status_code == 404):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='404-page-not-found')
        elif(request.status_code >= 400 and request.status_code < 500):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='4xx-client-response')
        elif(request.status_code >= 500):
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='5xx-server-response')
        else:
            print(f"[x] {domain} returned status code: {request.status_code}")
            return Page(domain=domain, status=request.status_code, header=header, redirected=redirect_location, element='unhandled-status-code')

    except Exception as e:
        print(f"[x] {domain} returned error: {e}")
        return Page(domain=domain, status=-1, header=header, redirected=redirect_location, element='exception-thrown')


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
    # print(f"[-] Parsing {domain}")
    page = fetch_dom(domain=domain, get_source=get_source,
                     output_path=output_path)
    if(page):
        page.set_domain_dns()
        return page
    return None


def export_json(*, output_path: str, collections: list):
    print(f"[-] Exporting to: {output_path}")
    with open(output_path, 'w') as output:
        output.writelines(json.dumps(
            [x.__dict__() for x in collections], indent=4, sort_keys=True))


def export_csv(*, output_path: str, collections: list):
    print(f"[-] Exporting to: {output_path}")
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Domain', 'A-records', 'Server',
                         'Status', 'Redirected To', 'Bucket', 'Matched On'])
        for collection in collections:
            for page in collection.pages:
                # Handle AWS slightly differently
                if(collection.name == "AWS Collection"):
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.status, page.redirected,
                                     collection.name, ", ".join(collection.get_match_for(page=page))])
                else:
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]), page.header, page.status, page.redirected,
                                     collection.name, ", ".join([matched for matched in page.matched if matched in collection.keywords])])


def process(*, input_path: str, collections: list, get_source: bool = True, output_path: str = '/tmp/') -> list:
    print(f"[-] Reading {input_path}")
    if get_source:
        print(f"[-] Downloading Page Source in: {output_path}")

    with open(input_path) as targets:
        domains = [target.strip() for target in targets.readlines()]

    with ThreadPoolExecutor(max_workers=50) as exc:
        pages = list(exc.map(lambda domain: parse_domain(
            domain=domain, get_source=get_source, output_path=output_path), domains))

    for collection in collections:
        for page in pages:
            collection.validate(page=page)

    if get_source:
        print(f"[*] Page Sources: {output_path}")

    return collections
