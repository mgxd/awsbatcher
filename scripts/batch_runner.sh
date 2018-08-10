#!/bin/bash

# Helper script to interact with AWS Batch submission

if [ $# -eq 0 ]; then
    echo "Missing arguments"
    exit 1
fi

if [[ -n "${S3_FILE_URL}" ]]; then
  BATCH_FILE=$(basename "${S3_FILE_URL}")
  # AWS will handle credentials
  aws s3 cp "${S3_FILE_URL}" "/usr/bin/${BATCH_FILE}"
  chmod +x "/usr/bin/${BATCH_FILE}"
  exec "${BATCH_FILE}" "${@}"
else
  echo 'Environ S3_FILE_URL is not defined'
  exit 1
fi
