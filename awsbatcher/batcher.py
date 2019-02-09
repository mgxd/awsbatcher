import os.path as op
import subprocess as sp

class AWSBatcher(dict):
    """
    Class to track and queue jobs in AWS Batch.
    Requires valid AWS CLI credentials
    """
    _cmd = ["aws", "batch", "submit-job"]

    def __init__(self,
                 desc,
                 dataset,
                 jobq,
                 jobdef,
                 vcpus=None,
                 mem_mb=None,
                 envars=None,
                 timeout=86400,
                 maxjobs=0,
                 **kwargs):
        """Dictionary class with AWS Batch CLI job submission capabilities"""
        super(AWSBatcher, self).__init__(**kwargs)
        self.desc = desc
        self.dataset = dataset
        self.jobq = jobq
        self.jobdef = jobdef
        self.vcpus = vcpus
        self.mem_mb = mem_mb
        self.envars = envars # usually set within job definition
        # allow overwriting
        if self.envars is None:
            self.envars = {}
        self.timeout = timeout
        self.maxjobs = maxjobs
        self._queued = 0


    @property
    def njobs(self):
        """Number of Batch master jobs"""
        return len(self.keys())


    def _gen_subcmd(self, dataset_url, array):
        """Generate an AWS CLI job submission command"""
        args = self._cmd[:]
        site = op.basename(dataset_url).lower()
        if len(array) < 1:
            print("No jobs found for", site)
            return

        jobname = "%s%s-%s" % (self.dataset, site, self.desc)
        args.extend(['--job-name', jobname,
                     '--job-queue', self.jobq,
                     '--job-definition', self.jobdef])

        if len(array) > 1:
            args.extend(['--array-properties', 'size=%d' % len(array)])

        overrides = []
        if self.vcpus:
            overrides.append('vpus=%d' % self.vcpus)
        if self.mem_mb:
            overrides.append('memory=%d' % self.mem_mb)
        # overwrite command
        overrides.append('command=%s,%s' % (dataset_url,
                                            ','.join(array)))
        if self.envars:
            overrides.append('environment=[%s]' % (
                ','.join(['{name=%s,value=%s}' % (k,v) for
                          k,v in self.envars.items()])
            ))

        if overrides:
            args.extend(['--container-overrides', ','.join(overrides)])
        # if array is under the max job size, return args
        return args if self._check_jobs(len(array)) else None


    def run(self, dry=False):
        """Submits Batch jobs through AWS CLI"""
        msg = "Spawning %d job arrays" % self.njobs
        if self.njobs == 1:
            msg = msg[:-1]
        elif self.njobs < 1:
            return

        for key, vals in self.items():
            # check if values are chunks
            if isinstance(vals[0], tuple):
                for chunk in vals:
                    self._queue(key, chunk, dry)
            else:
                self._queue(key, vals, dry)

    def _run_cmd(self, cmd, dry=False):
        """Actual subprocess call"""
        if not cmd or not isinstance(cmd, list):
            raise RuntimeError("Invalid command")
        if dry:
            print(' '.join(cmd))
            return
        return sp.run(cmd, check=True, encoding='utf-8', stdout=sp.PIPE).stdout


    def _check_jobs(self, jobs):
        """If cap is set, do not queue more than cap"""
        if self.maxjobs < 1:
            self._queued += jobs
            return True
        elif self._queued + jobs > self.maxjobs:
            return False
        self._queued += jobs
        return True

    def _queue(self, site, subjects, dry=False):
        cmd = self._gen_subcmd(site, subjects)
        out = self._run_cmd(cmd, dry=dry)
        print('Queued so far:', self._queued)
