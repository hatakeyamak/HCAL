#!/bin/bash

echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc7_amd64_gcc700
echo $SCRAM_ARCH
eval `scramv1 project CMSSW CMSSW_10_6_12`
cd CMSSW_10_6_12/src
eval `scramv1 runtime -sh`
git cms-init --upstream-only
git cms-addpkg RecoLocalCalo/HcalRecProducers
git cms-addpkg RecoLocalCalo/HcalRecAlgos
git clone -b CMSSW_10_6_x https://github.com/wang-hui/HCAL.git
mv HCAL/Modified_files/samplingFactor.h RecoLocalCalo/HcalRecProducers/src
mv HCAL/Modified_files/HBHEPhase1Reconstructor.cc RecoLocalCalo/HcalRecProducers/src
mv HCAL/Modified_files/BuildFile.xml RecoLocalCalo/HcalRecProducers
mv HCAL/Modified_files/SimpleHBHEPhase1Algo.cc RecoLocalCalo/HcalRecAlgos/src
mv HCAL/Modified_files/parseHBHEPhase1AlgoDescription.cc RecoLocalCalo/HcalRecAlgos/src
mv ${_CONDOR_SCRATCH_DIR}/HBHEPhase1Reconstructor_cfi.py RecoLocalCalo/HcalRecProducers/python
scram b -j 4
cd HCAL
mv ${_CONDOR_SCRATCH_DIR}/reco_MC_RAW2DIGI_RECO.py .
mv ${_CONDOR_SCRATCH_DIR}/FileList.tar .
tar -xvf FileList.tar
pwd

mkdir results_temp
cmsRun reco_MC_RAW2DIGI_RECO.py $1 > results_temp/reco_MC.stdout

mkdir split_file
python split_file.py

#python add_gen_energy.py
#python compare_gen_reco.py
python add_gen_energy_2d.py
#python compare_gen_reco_2d.py

xrdcp results_temp/reco_MC.stdout root://cmseos.fnal.gov//${2}/reco_MC_${3}.stdout
#xrdcp results_temp/RECO_MC.root root://cmseos.fnal.gov//${2}/RECO_MC_${3}.root
#xrdcp results_temp/result.csv root://cmseos.fnal.gov//${2}/result_${3}.csv
#xrdcp results_temp/result_origin.root root://cmseos.fnal.gov//${2}/result_${3}.root
xrdcp results_temp/result_2d.csv root://cmseos.fnal.gov//${2}/result_2d_${3}.csv
#xrdcp results_temp/result_2d.root root://cmseos.fnal.gov//${2}/result_2d_${3}.root
