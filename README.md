# Setup instructions
cmsrel CMSSW_10_0_3  
cd CMSSW_10_0_3/src  
cmsenv  
git cms-init  
git cms-merge-topic 22291
git cms-addpkg L1Trigger/L1TCalorimeter  
cd L1Trigger  
git clone -b 1003_ECAL https://github.com/jjbuchanan/CaloLayer1Calibrations.git  
cd ..  
scram b -j 8  
