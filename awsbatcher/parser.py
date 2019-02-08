import os.path as op
import requests

import boto3
from bs4 import BeautifulSoup

def fetch_datalad_subjects(site_url):
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


def fetch_datalad_data(project_url, batcher, single_site=False):
    """
    Crawls target dataset on DataLad's server.

    Parameters
    ----------
    project_url : string
        URL to DataLad project
    batcher : object
        Initialized AWSBatcher object
    single_site : boolean, optional
        Only submit single site

    Returns
    -------
    AWSBatcher: object
    Enhanced Dictionary consisting of:
        - site location keys
        - list of subjects values
    """
    if single_site:
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
                batcher[site_url] = fetch_datalad_subjects(site_url)
    return batcher

def fetch_s3_subjects(s3_client, bucket, site_url):
    """
    Crawls S3 directory and returns any subjects found.
    """
    res = s3_client.list_objects(Bucket=bucket, Prefix=site_url, Delimiter='/')
    # relative to bucket root, need just sub-<>
    subjects = []
    for s in res.get("CommonPrefixes"):
        subj = op.basename(s.get("Prefix")[:-1])
        if subj.startswith('sub-'):
            subjects.append(subj)
    return subjects


def fetch_s3_data(s3_url, batcher):
    """
    Crawls BIDS directory in S3 bucket.
    """
    bpath = ""
    s3_path = s3_url[5:].split('/', 1)
    if len(s3_path) == 2:
        bpath = s3_path[1]
    bucket = s3_path[0]

    s3_client = boto3.client('s3')
    samples = s3_client.list_objects(Bucket=bucket, Prefix=bpath, Delimiter='/')
    for res in samples.get('CommonPrefixes'):
        # relative path from bucket root
        site = res.get('Prefix')
        if site.endswith('/'):
            key = op.basename(site[:-1])
            rel_site_path = bpath + key + '/' # needs trailing space
            abs_site_path = s3_url + key + '/'
            batcher[abs_site_path] = fetch_s3_subjects(s3_client, bucket, rel_site_path)
    return batcher
