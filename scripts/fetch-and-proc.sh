#!/bin/bash

# install a datalad data repository for fmriprep processing
# and push results to S3 bucket

set -e

DATASET=$2

if [[ -n ${AWS_BATCH_JOB_ARRAY_INDEX} ]]; then
  # job array
  subjidx=$(expr ${AWS_BATCH_JOB_ARRAY_INDEX} + 2)
  SUBJECT=${!subjidx}
else
  # single job
  SUBJECT=$3
fi

if [[ -z ${DATASET} ]] || [[ -z ${SUBJECT} ]]; then
  echo "Dataset or subject not properly specified"
  exit 1
fi

# set this via CLI
S3_BUCKET="s3://gablab-fmriprep"

# first, check if subject has already been processed
aws s3 ls ${S3_BUCKET}/derivatives/fmriprep | grep ${SUBJECT} &> /dev/null
if [ $? == 0 ] && [[ -z ${S3_OVERWRITE} ]]; then
  echo "${SUBJECT} has already been processed - set S3_OVERWRITE env to rerun"
  exit 0
fi

# make data directory
mkdir data && pushd data
# first install the remote repository
datalad install -r ${DATASET}
# now fetch only files necessary for single subject fmriprep
datalad get -r -J 8 ./*/${SUBJECT}/{func,anat}/* ./*/${SUBJECT}/*/{func,anat}/* ./*/*.json || true
# return to project root
popd


# ensure derivatives exists
if [ ! -d derivatives ]; then
    mkdir derivatives
fi

# make working directory
if [ ! -d scratch ]; then
    mkdir scratch
fi

datadir=$(ls $(pwd)/data/* -d)

# preprocess data
cmd="fmriprep ${datadir} derivatives participant \
    --participant_label ${SUBJECT} --cifti-output \
    --nthreads 8 --mem_mb 10000 --output-space template \
    --template-resampling-grid 2mm --ignore slicetiming \
    -w scratch --fs-license-file /tmp/.fs_license.txt"

echo "Command: ${cmd}"
eval ${cmd}

# save outputs to S3 bucket
aws s3 cp derivatives/ ${S3_BUCKET}/derivatives --recursive --exclude "freesurfer/*"
exit 0
