import requests
from requests.adapters import HTTPAdapter, Retry
import json
import re
import sys
import pandas as pd


def echo(n: int):
    for i in range(n):
        print(i)


def get_next_link(headers):
    if "Link" in headers:
        links = headers["Link"].split(",")
        for link in links:
            match = re.search(r'<(.+)>; rel="next"', link)
            if match:
                return match.group(1)
    return None


def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        total = response.headers.get("x-total-results")
        yield response, total
        batch_url = get_next_link(response.headers)


def get_kingdom(entry):
    if "Fungi" in entry["organism"]["lineage"]:
        kd = "Fungi"
    elif "Viridiplantae" in entry["organism"]["lineage"]:
        kd = "Viridiplantae"
    elif "Metazoa" in entry["organism"]["lineage"]:
        kd = "Metazoa"
    else:
        kd = "Other"
    return kd
