#!/bin/sh
export pwd=/nfs_scratch/jjbuchanan/calibrations_Jan2017/MonteCarlo/CMSSW_9_2_8/src
cat>Job_${3}_${5}_to_${6}.sh<<EOF
#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /nfs_scratch/jjbuchanan/calibrations_Jan2017/MonteCarlo/CMSSW_9_2_8/src
cmsenv
cd \${_CONDOR_SCRATCH_DIR}
python ${1} ${2} ${3} ${4} ${5} ${6}
EOF

chmod 775 Job_${3}_${5}_to_${6}.sh

cat>condor_${3}_${5}_to_${6}<<EOF
x509userproxy = /tmp/x509up_u4321
universe = vanilla
Executable = Job_${3}_${5}_to_${6}.sh
Notification         = never
WhenToTransferOutput = On_Exit
ShouldTransferFiles  = yes
Requirements = (TARGET.UidDomain == "hep.wisc.edu" && TARGET.HAS_CMS_HDFS)
on_exit_remove       = (ExitBySignal == FALSE && (ExitCode == 0 || ExitCode == 42 || NumJobStarts>3))
+IsFastQueueJob      = True
getenv = true
request_memory       = 1992
request_disk         = 2048000
Transfer_Input_Files = ${1}
output               = \$(Cluster)_\$(Process)_${3}_${5}_to_${6}.out
error                = \$(Cluster)_\$(Process)_${3}_${5}_to_${6}.err
Log                  = \$(Cluster)_\$(Process)_${3}_${5}_to_${6}.log
Queue
EOF

condor_submit condor_${3}_${5}_to_${6}
