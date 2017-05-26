# Setup instructions
cmsrel CMSSW_9_2_0  
cd CMSSW_9_2_0/src  
cmsenv  
git cms-init  
git cms-merge-topic 18869  
git cms-addpkg L1Trigger/L1TCalorimeter  
cd L1Trigger  
git clone https://github.com/jjbuchanan/CaloLayer1Calibrations.git  
cd ..  
scram b -j 8  
