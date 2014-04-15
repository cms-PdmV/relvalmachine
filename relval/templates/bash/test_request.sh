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

mkdir -p json_data
cp ../../json_data/* json_data

scram b -j 2

runTheMatrix.py {{run_the_matrix_conf}}