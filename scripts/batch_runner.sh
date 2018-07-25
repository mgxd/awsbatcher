#!/bin/bash

# Helper script to interact with AWS Batch submission

if [ $# -eq 0 ]; then
    echo "Missing arguments"
    exit 1
fi

set -eu

BATCH_FILE=$(basename ${S3_FILE_URL})

# AWS will handle credentials
aws s3 cp ${S3_FILE_URL} "/${BATCH_FILE}"
chmod +x "/${BATCH_FILE}"

exec "/${BATCH_FILE}" "${@}"
