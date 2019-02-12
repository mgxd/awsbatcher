__version__ = "0.0.1-dev"
__package__ = "awsbatcher"
__desc__ = "CLI to simplify ODP AWSBatch submissions"
__url__ = "https://github.com/mgxd/aws-batcher"
__author__ = "Mathias Goncalves"
__email__ = "mathiasg@mit.edu"
__requires__ = [
    "requests",
    "bs4",
    "boto3",
    "lxml",
]
__tests_requires__ = [
    "pytest",
    "moto",
]

__extra_requires__ = {
    "tests": __tests_requires__,
}
