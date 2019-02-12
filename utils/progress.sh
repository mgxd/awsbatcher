#!/bin/bash
# parse output S3 buckets to extract processing information

# | DATASET | PROCESS | BUCKET | # PARTICIPANTS | # COMPLETE | # FAILED |

OUTFILE="./s3_outputs.tsv"

if [ -f ${OUTFILE} ]; then
  echo "Existing output found - remove to rerun"
  exit 1
fi

printf "Dataset\tProcess\tBucket_URL\tSubjects\tCompleted\tFailed\n" > ${OUTFILE}
# TODO: grab total from awsbatcher --dry submissions

DATASETS=(abide abide2 adhd200 corr hbn openneuro)
#DATASETS=(openneuro)
PROCESS=(denoise mindboggle simple_workflow mriqc fmriprep fmriprep-legacy)
#PROCESS=(fmriprep)

# OUTPUTS
##################################################
# denoise (derivatives) -> subject directory exists
# mindboggle (derivatives) -> mindboggled directory exists 
# simple workflow -> JSON file exists
# mriqc -> subject folder exists
# fmriprep -> HTML report

# fmriprep -> check for subject folder. If log/ exists within, it errored at some point

function getCount() {
  OCOUNT=0
  case ${2} in
  mindboggle)
    OCOUNT=$(aws s3 ls ${1}/derivatives/${2}/mindboggled/ | wc -l)
    ;;
  simple_workflow)
    OCOUNT=$(aws s3 ls ${1}/derivatives/${2}/ --recursive | grep segstats.json | wc -l)
    ;;
  fmriprep)
    # iter within each subject
#    SUBJS=$(aws s3 ls ${1}/derivatives/fmriprep/ | grep "PRE" | grep "sub-*" | awk '{print $2}')
#    for SUBJ in ${SUBJS[@]}; do
#      if [[ -z $(aws s3 ls ${1}/derivatives/fmriprep/${SUBJ%?}/log) ]]; then
#        OCOUNT=$((OCOUNT+1))
#      fi
#    done
    OCOUNT=$(aws s3 ls ${1}/derivatives/fmriprep/ | grep ".html" | wc -l)
    ;;
  *)
    # mriqc, denoise
    OCOUNT=$(aws s3 ls ${1}/derivatives/${2}/ | grep PRE | wc -l)
    ;;
  esac
  
  echo ${OCOUNT}
}

for PROC in ${PROCESS[@]}; do
  for DATASET in ${DATASETS[@]}; do

    COUNT=0
    BUCKET="s3://${DATASET}-${PROC}"
    if [[ ${PROC} == "simple_workflow" ]]; then
      BUCKET="s3://${DATASET}-mindboggle"
    fi

    if [[ ${DATASET} = "openneuro" ]]; then
      for SITE in $(aws s3 ls ${BUCKET} | awk '{print $2}' | grep ds*); do
        SBUCKET="${BUCKET}/${SITE%?}"
        TMP=0
        if $(aws s3 ls ${SBUCKET} &> /dev/null); then
          TMP=$(getCount ${SBUCKET} ${PROC})
          echo ${SBUCKET} ${TMP}
        fi
        COUNT=$((COUNT + TMP))
      done
      echo Finished ${BUCKET}: ${COUNT}

    else
      if aws s3 ls ${BUCKET} &> /dev/null; then
        echo ${BUCKET}
        COUNT=$(getCount ${BUCKET} ${PROC})
      fi
    fi

    [ ${COUNT} -gt 0 ] && echo ${COUNT}

    printf "${DATASET}\t${PROC}\t${BUCKET}\tTODO\t${COUNT}\tTODO\n" >> ${OUTFILE}
    
  done
done
