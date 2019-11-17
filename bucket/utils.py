#!/bin/python3

import json
import urllib3
import requests
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr.ip import IPAddress, IPNetwork
from .page import Page

urllib3.disable_warnings()

AWS_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def fetch_dom(*, domain: str, get_source: bool = False, output_path: str = 'output/sources/') -> Page:
    """ Fetch DOM element for domain """
    # session = HTMLSession(verify=False)
    try:
        new_domain = domain

        if 'http' not in domain:
            new_domain = f"https://{domain}"

        try:
            # r = session.get(new_domain)
            request = requests.get(
                new_domain, verify=False, allow_redirects=True)
        except:
            new_domain = f"http://{domain}"
            # r = session.get(new_domain)
            request = requests.get(
                new_domain, verify=False, allow_redirects=True)

            # r.html.render()

        if(request.status_code >= 200 and request.status_code < 400):
            if(get_source):
                with open(f"{output_path}{domain.replace('/', '').replace(':', '')}.txt", 'w') as file:
                    file.writelines(request.content.decode().lower())
            return Page(domain=domain, element=request.content.decode().lower())
        elif(request.status_code == 401):
            return Page(domain=domain, element='login')
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


def parse_domain(*, domain: str, get_source: bool = False, output_path: str = 'output/sources/') -> Page:
    # print(f"[-] Parsing {domain}")
    page = fetch_dom(domain=domain, get_source=get_source,
                     output_path=output_path)
    if(page):
        page.set_domain_dns()
        return page
    return None


def run(*, input_path: str, output_json: str, collections: list(), get_source: bool = False, output_path: str = 'output/sources/'):
    print(f"[-] Reading {input_path}")

    if get_source:
        print(f"[-] Downloading Page Source in: {output_path}")

    with open(input_path) as targets:
        for target in targets.readlines():
            domain = target.strip()
            page = parse_domain(
                domain=domain, get_source=get_source, output_path=output_path)
            with ThreadPoolExecutor(max_workers=5) as exc:
                list(exc.map(lambda collection: collection.validate(
                    page=page), collections))

    with open(output_json, 'w') as output:
        output.writelines(json.dumps([x.__dict__()
                                      for x in collections], indent=4))

    if get_source:
        print(f"[-] Page Sources: {output_path}")
    print(f"[-] Completed: {output_json}")
