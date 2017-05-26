#!/bin/bash

# Submit efficiency ntuple jobs on the mu+jet skim
EXPECTED_ARGS=1
if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0 JOB_NAME"
fi

farmoutAnalysisJobs $1 \
  --infer-cmssw-path \
  --input-dbs-path=/SinglePion_PT200to500/RunIISpring16DR80-NoPURAW_NZS_withHLT_80X_mcRun2_asymptotic_v14-v1/GEN-SIM-RAW \
  --assume-input-files-exist \
  ./piMinus_submit_cfg.py  \
  'inputFiles=$inputFileNames' 'outputFile=$outputFileName'

