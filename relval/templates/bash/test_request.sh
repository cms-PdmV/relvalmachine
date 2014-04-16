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

git cms-addpkg Configuration/PyReleaseValidation
yes | cp  -rf /afs/cern.ch/user/z/zgatelis/public/CMSSW_7_1_0_pre4/src/Configuration/PyReleaseValidation/python/* Configuration/PyReleaseValidation/python/

scram b -j 2

mkdir -p json_data
cern-get-sso-cookie -u {{hostname}} -o relvalmachine-cookie.txt --krb
curl -s -k -o json_data/{{id}}.json {{hostname}}/api/conf/tests/{{id}} --cookie relvalmachine-cookie.txt


runTheMatrix.py {{run_the_matrix_conf}}