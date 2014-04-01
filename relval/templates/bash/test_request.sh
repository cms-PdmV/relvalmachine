#!/bin/bash
source  /afs/cern.ch/cms/cmsset_default.sh

if [ -r {{cmssw_request}}/src ] ; then
 echo release {{cmssw_request}} already exists
else
scram p CMSSW {{cmssw_request}}
fi
cd {{cmssw_request}}/src
eval `scram runtime -sh`

scram b
cd ../../
cmsDriver.py Configuration/GenProduction/python/B2G-Summer12-00461-fragment.py --filein "dbs:/Bprime_M-500_8TeV-madgraph/Summer12-START53_V7C-v1/GEN" --fileout file:B2G-Summer12-00461.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions START53_V7C::All --beamspot Realistic8TeVCollision --step GEN,SIM --python_filename B2G-Summer12-00461_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 0 || exit $? ;
cmsRun -e -j B2G-Summer12-00461_rt.xml B2G-Summer12-00461_1_cfg.py || exit $? ;