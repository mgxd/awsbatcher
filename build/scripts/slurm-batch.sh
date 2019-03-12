#!/bin/bash

#SBATCH --mem=14GB
#SBATCH --cpus-per-task=8
#SBATCH --time=2-00:00:00
#SBATCH --qos=use-everything

if [ $# -eq 0 ]; then
  echo "No arguments passed"
  exit 1
fi

# set any images / variables
IMG="/storage/gablab001/data/singularity-images/test/aws/aws-mindboggle.sif"

# set envirnomental variables
JOBTYPE="fmriprep"
AWSBATCH_CPUS=8
AWSBATCH_MEM_MB=14000
S3_FILE_URL="s3://gitlab-spooky-cache/fetch-and-proc"
S3_BUCKET="s3://hbn-mindboggle"

# set local working directory
# should be unique for each subject
WORKDIR="/om/scratch/`whoami`/awsbatcher/${JOBTYPE}"

CMD="singularity run -B ${WORKDIR}:/working ${IMG} $@"
printf "Command:\n${CMD}\n"
${CMD}
