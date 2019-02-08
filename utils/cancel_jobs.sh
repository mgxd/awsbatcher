#!/bin/bash

set -eu

QUEUE=${1}

# cancel all
STATES=(SUBMITTED PENDING RUNNABLE STARTING RUNNING)

printf "Enter reason for canceling jobs below:\n"
read REASON

for STATE in ${STATES[@]}; do
    for JOB in $(aws batch list-jobs --job-queue ${QUEUE} --no-paginate --job-status ${STATE} | jq -r ".jobSummaryList[].jobId"); do
        aws batch cancel-job --job-id ${JOB} --reason "${REASON}"
        aws batch terminate-job --job-id ${JOB} --reason "${REASON}"
        echo "Job ${JOB} (STATE: ${STATE}) removed from queue ${QUEUE}"
    done
done
