"""Main script to initiate jobs"""

from argparse import ArgumentParser, Action

from awsbatcher import DATALAD_ROOT, PROJECTS_DIR, __version__
from awsbatcher.parser import fetch_datalad_data, fetch_s3_data
from awsbatcher.batcher import AWSBatcher, SLURMBatcher

class Str2DictAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        val = dict(val.split('=') for val in values.split(','))
        setattr(namespace, self.dest, val)

def get_parser():
    docstr = "awsbatcher: odp batch jobs made simple"
    parser = ArgumentParser()
    parser.add_argument('--version', action='version', version=__version__)
    # Mandatory arguments
    parser.add_argument('project',
                        help="Datalad project name or path to S3 bucket. "
                        "Supported projects include {}, and openneuro:<project>"
                        .format(", ".join(PROJECTS_DIR.keys())))
    parser.add_argument('batcher', choices=('aws', 'slurm'),
                        help="Batching system to submit to - supported include"
                             "`aws` and `slurm`")
    aws = parser.add_argument_group('aws')
    aws.add_argument('--aws-queue', help="AWS Batch job queue")
    aws.add_argument('--aws-def', help="AWS Batch job definition")
    slurm = parser.add_argument_group('slurm')
    slurm.add_argument('--bscript', help="SLURM batch script")
    # Optional job definition overwrites
    jobdef = parser.add_argument_group('job-definitions')
    jobdef.add_argument('--vcpus', type=int, help='Number of vCPUs')
    jobdef.add_argument('--mem-mb', type=int, help='Requested memory (MB)')
    jobdef.add_argument('--envars', action=Str2DictAction,
                        help="One or more environmental variables defined as "
                             "KEY=VALUE and comma-separated")
    jobdef.add_argument('--timeout', type=int, help='Time until timeout (sec)')
    # Optional arguments
    parser.add_argument('--desc', default='awsbatcher', help="Job description")
    parser.add_argument('--maxjobs',
                        type=int,
                        default=0,
                        help="Max number of queued jobs (No limit = set to 0)")
    parser.add_argument('--dry',
                        action='store_true',
                        default=False,
                        help='Print to console instead of submitting')
    return parser

def main(argv=None):
    parser = get_parser()
    args = parser.parse_args(argv)
    # allow single site submission or entire dataset
    single_site = False
    is_s3 = False

    # allow S3 + datalad
    if ':' in args.project:
        args.project, secondarydir = args.project.split(':', 1)
        single_site = True
        project_url = '/'.join([DATALAD_ROOT, args.project, secondarydir])
    else:
        try:
            secondarydir = PROJECTS_DIR[args.project]
            project_url = '/'.join([DATALAD_ROOT, args.project, secondarydir])
        except:
            raise KeyError("Project", args.project, "not found")
        # check for S3 bucket
        if secondarydir.startswith("s3://"):
            is_s3 = True
            project_url = secondarydir

    # define our Batcher
    if args.batcher == 'aws':
        batcher = AWSBatcher(dataset=args.project,
                             jobq=args.aws_queue,
                             jobdef=args.aws_def,
                             desc=args.desc,
                             vcpus=args.vcpus,
                             mem_mb=args.mem_mb,
                             envars=args.envars,
                             timeout=args.timeout,
                             maxjobs=args.maxjobs)
    elif args.batcher == 'slurm':
        batcher = SLURMBatcher(dataset=args.project,
                               bscript=args.bscript,
                               desc=args.desc)

    # crawl and aggregate subjects to run
    if is_s3:
        batcher = fetch_s3_data(project_url, batcher)
    else:
        batcher = fetch_datalad_data(project_url, batcher, single_site)

    # run the batcher
    batcher.run(dry=args.dry)

if __name__ == '__main__':
    main()
