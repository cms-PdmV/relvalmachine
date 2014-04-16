#!/bin/bash

mkdir -p {{directory}}
cd {{directory}}

source  /afs/cern.ch/cms/cmsset_default.sh

if [ -r {{cmssw_release}}/src ] ; then
  echo release {{cmssw_release}} already exists
else
  scram p CMSSW {{cmssw_release}}
fi
cd {{cmssw_release}}/src

eval `scramv1 runtime -sh`

mkdir -p json_data
cern-get-sso-cookie -u https://cms-pdmv-dev.cern.ch/relvalmachine/ -o relvalmachine-cookie.txt --krb
curl -s -k -o json_data/{{id}}.json https://cms-pdmv-dev.cern.ch/relvalmachine/api/conf/{{id}} --cookie relvalmachine-cookie.txt


git cms-addpkg Configuration/PyReleaseValidation
yes | cp  -rf /afs/cern.ch/user/z/zgatelis/public/CMSSW_7_1_0_pre4/src/Configuration/PyReleaseValidation/python/* Configuration/PyReleaseValidation/python/

scram b -j 2

runTheMatrix.py {{run_the_matrix_conf}}