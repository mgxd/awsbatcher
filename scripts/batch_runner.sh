#!/bin/bash

# Helper script to interact with AWS Batch submission

if [ $# -eq 0 ]; then
    echo "Missing arguments"
    exit 1
fi

if [[ -n "${S3_BUCKET}" ]]; then
  # copy to S3 bucket
  SRC=$1
  aws s3 cp "${SRC}" "${S3_BUCKET}"
elif [[ -n "${S3_FILE_URL}" ]]; then
  BATCH_FILE=$(basename "${S3_FILE_URL}")
  # AWS will handle credentials
  aws s3 cp "${S3_FILE_URL}" "/${BATCH_FILE}"
  chmod +x "/${BATCH_FILE}"
  exec "/${BATCH_FILE}" "${@}"
else
  echo 'Neither $S3_BUCKET or $S3_FILE_URL are defined'
  exit 1
fi
