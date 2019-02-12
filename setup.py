import os.path as op
from setuptools import setup, find_packages

ldict = locals()
ver_file = op.join(op.dirname(__file__), 'awsbatcher', 'info.py')
with open(ver_file) as infofile:
    exec(infofile.read(), globals(), ldict)

setup(
    name=ldict['__package__'],
    version=ldict['__version__'],
    description=ldict['__desc__'],
    url=ldict['__url__'],
    author=ldict['__author__'],
    author_email=ldict['__email__'],
    packages=find_packages(),
    install_requires=ldict['__requires__'],
    tests_require=ldict['__tests_requires__'],
    extras_require=ldict['__extra_requires__'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            'awsbatcher=awsbatcher.cli.run:main',
        ],
    },
)
