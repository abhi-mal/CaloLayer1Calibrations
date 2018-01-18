# Setup instructions
cmsrel CMSSW_9_4_0_patch1  
cd CMSSW_9_4_0_patch1/src  
cmsenv  
git cms-init  
git cms-addpkg L1Trigger/L1TCalorimeter  
cd L1Trigger  
git clone https://github.com/jjbuchanan/CaloLayer1Calibrations.git  
cd ..  
scram b -j 8  
