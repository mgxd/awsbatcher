import os

DATALAD_ROOT = 'http://datasets-tests.datalad.org'

PROJECTS_DIR = {
    'abide': 'RawDataBIDS',
    'abide2': 'RawData',
    'adhd200': 'RawDataBIDS',
}

batch_template = os.path.join(os.path.dirname(__file__), 'batch-skeleton.json')
