#!/bin/bash

# Submit efficiency ntuple jobs on the mu+jet skim
EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 JOB_NAME"
fi

farmoutAnalysisJobs $1 \
  --infer-cmssw-path \
  --input-dbs-path=/SinglePion_PT200to500/PhaseISpring17DR-NoPUNZS_90X_upgrade2017_realistic_v20_ext1-v1/GEN-SIM-RAW \
  --assume-input-files-exist \
  ./piMinus_submit_cfg.py  \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName'

