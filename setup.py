from setuptools import setup, find_packages

# TODO: migrate to aws-batcher/info.py
__version__ = "0.0.1-dev"
__desc__ = "CLI to simply AWS batch submissions"
__url__ = "https://github.com/mgxd/aws-batcher"
__requires__ = [
    "requests",
    "bs4",
]

setup(
    name='awsbatcher',
    version=__version__,
    description=__desc__,
    url=__url__,
    author="Mathias Goncalves",
    author_email="mathiasg@mit.edu",
    packages=find_packages(),
    install_requires=__requires__,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'awsbatcher=awsbatcher.cli.run:main',
        ],
    },
)
