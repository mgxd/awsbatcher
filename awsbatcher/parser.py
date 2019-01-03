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


def fetch_data(project_url, batcher, openneuro=False):
    """
    Crawls target dataset on DataLad's server.

    Parameters
    ----------
    project_url : string
        URL to DataLad project
    batcher : object
        Initialized AWSBatcher object

    Returns
    -------
    AWSBatcher: object
    Enhanced Dictionary consisting of:
        - site location keys
        - list of subjects values
    """
    if openneuro:
        batcher[project_url] = fetch_subjects(project_url)
    else:
        res = requests.get(project_url)
        soup = BeautifulSoup(res.content, 'lxml')
        samples = soup.find_all("a")

        for a in samples:
            title = a.string.strip()
            if title[-1].endswith('/'):
                site = title[:-1]
                site_url = project_url + '/' + site
                batcher[site_url] = fetch_subjects(site_url)
    return batcher
