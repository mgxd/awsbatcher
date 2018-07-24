import os.path as op

import requests
from bs4 import BeautifulSoup

def fetch_subjects(site_url):
    """
    Crawls site directory and aggregates subjects

    Parameters
    ----------
    site_url : URL string

    Returns
    -------
    subjects : list
        List of site subjects in BIDS format
    """
    res = requests.get(site_url)
    soup = BeautifulSoup(res.content, 'lxml')
    return [s.string[:-1] for s in soup.find_all("a") if s.string.startswith('sub')]


def fetch_data(project_url):
    """
    Crawls target dataset on Datalad's website.

    Parameters
    ----------
    project_url : URL string

    Returns
    -------
    data : dict
        Dictionary consisting of:
        - site location keys
        - list of subjects values
    """
    res = requests.get(project_url)
    soup = BeautifulSoup(res.content, 'lxml')
    samples = soup.find_all("a")

    data = {}
    for a in samples:
        title = a.string.strip()
        if title[-1].endswith('/'):
            site = title[:-1]
            site_url = op.join(project_url, site)
            data[site_url] = fetch_subjects(site_url)
    return data
