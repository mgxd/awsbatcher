"""Main script to initiate jobs"""

from argparse import ArgumentParser

from awsbatcher import DATALAD_ROOT, PROJECTS_DIR
from awsbatcher.parser import fetch_data

def main():
    parser = ArgumentParser()
    parser.add_argument('project', choices=['abide', 'abide2'],
                        help="Datalad project")
    args = parser.parse_args()

    project_url = "%s/%s/%s" % (DATALAD_ROOT,
                                args.project,
                                PROJECTS_DIR[args.project])

    # first crawl and aggregate subjects to run
    data = fetch_data(project_url)

if __name__ == '__main__':
    main()
