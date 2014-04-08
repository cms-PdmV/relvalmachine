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
eval `scram runtime -sh`

scram b
cd ../../


{% for step in steps %}
{{step.text}} -n {{step.events_num}} || exit $? ;
{% endfor %}


cmsRun -e -j B2G-Summer12-00460_rt.xml B2G-Summer12-00460_1_cfg.py || exit $? ;