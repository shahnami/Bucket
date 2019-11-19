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
requests.adapters.DEFAULT_RETRIES = 1

AWS_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def fetch_dom(*, domain: str, get_source: bool = True, output_path: str = '/tmp/') -> Page:
    """ Fetch DOM element for domain """
    # session = HTMLSession(verify=False)
    try:
        new_domain = domain

        if 'http' not in domain:
            new_domain = f"https://{domain}"

        try:
            request = requests.get(
                new_domain, verify=False, allow_redirects=True, timeout=5)
        except:
            new_domain = f"http://{domain}"
            request = requests.get(
                new_domain, verify=False, allow_redirects=True, timeout=5)

        if(request.status_code >= 200 and request.status_code < 400):
            if(get_source):
                with open(f"{output_path}{domain.replace('/', '').replace(':', '')}.txt", 'w') as file:
                    file.writelines(request.content.decode().lower())
            return Page(domain=domain, element=request.content.decode().lower())
        elif(request.status_code == 401):
            return Page(domain=domain, element='login, 4xx-client-error')
        elif(request.status_code == 402):
            return Page(domain=domain, element='payment, 4xx-client-error')
        elif(request.status_code == 404):
            return Page(domain=domain, element='404-page-not-found')
        elif(request.status_code >= 400 and request.status_code < 500):
            return Page(domain=domain, element='4xx-client-error')
        elif(request.status_code >= 500):
            return Page(domain=domain, element='5xx-server-error')
        else:
            print(f"[x] {domain} returned status code: {request.status_code}")
            return Page(domain=domain, element='none')

    except Exception as e:
        print(f"[x] {domain} returned error: {e}")
        return Page(domain=domain, element='none')


def get_aws_ranges(*, url: str = AWS_URL) -> list:
    print(f"[-] Fetching AWS ranges {url}")
    aws_ranges = list()
    aws = list()

    with requests.get(url) as req:
        aws_ranges = json.loads(req.content.decode())

    for prefix in aws_ranges['prefixes']:
        aws.append(IPNetwork(prefix['ip_prefix']))
    return aws


def parse_domain(*, domain: str, get_source: bool = True, output_path: str = '/tmp/') -> Page:
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

        writer.writerow(['Domain', 'A-records', 'Bucket', 'Matched On'])
        for collection in collections:
            for page in collection.pages:
                # Handle AWS slightly differently
                if(collection.name == "AWS Collection"):
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]),
                                     collection.name, ", ".join(collection.get_match_for(page=page))])
                else:
                    writer.writerow([page.domain, ", ".join([str(ip) for ip in page.ip]),
                                     collection.name, ", ".join([matched for matched in page.matched if matched in collection.keywords])])


def process(*, input_path: str, collections: list, get_source: bool = True, output_path: str = '/tmp/') -> list:
    print(f"[-] Reading {input_path}")
    if get_source:
        print(f"[-] Downloading Page Source in: {output_path}")

    with open(input_path) as targets:
        domains = [target.strip() for target in targets.readlines()]

    with ThreadPoolExecutor(max_workers=10) as exc:
        pages = list(exc.map(lambda domain: parse_domain(
            domain=domain, get_source=get_source, output_path=output_path), domains))

        for collection in collections:
            for page in pages:
                collection.validate(page=page)

    if get_source:
        print(f"[*] Page Sources: {output_path}")

    return collections
