#!/bin/bash


STEP_TITLE="working-step"

curl -X POST -H "Content-Type: application/json" -d '{"title": "'$STEP_TITLE'", "name": "Configuration/GenProduction/python/B2G-Summer12-00460-fragment.py", "immutable": false, "parameters": [{"flag": "--filein", "value": "\"dbs:/Bprime_M-500_8TeV-madgraph/Summer12-START53_V7C-v1/GEN\""}, {"flag": "--fileout", "value": "file:B2G-Summer12-00460.root"}, {"flag": "--mc", "value": ""}, {"flag": "--eventcontent", "value": "RAWSIM"}, {"flag": "--datatier", "value": "GEN-SIM"}, {"flag": "--conditions", "value": "START53_V7C::All"}, {"flag": "--beamspot", "value": "Realistic8TeVCollision"},  {"flag": "--step", "value": "GEN,SIM"}, {"flag": "--python_filename", "value": "B2G-Summer12-00460_1_cfg.py"}, {"flag": "--no_exec", "value": ""}, {"flag": "--customise", "value": "Configuration/DataProcessing/Utils.addMonitoring"}], "type": "default"}' http://localhost:8000/api/steps;


STEP_ID=`curl -X GET -i -s -H "Accept: application/json"  'http://localhost:8000/api/steps?search='$STEP_TITLE | tr , "\n" | grep id | sed 's/"id": "\([^"]*\).*/\1/' | sed 's/ //g'`



curl -X POST -H "Content-Type: application/json" -d '{"label": "working-request", "description": "This request should work for testing", "type": "MC", "immutable": false, "steps": [{"id":'$STEP_ID'}], "cmssw_release": "CMSSW_5_3_11_patch2"}' http://localhost:8000/api/requests;


# Second step
STEP_TITLE="working-runTheMatrix-20"

curl -X POST -H "Content-Type: application/json" -d '{"title": "'$STEP_TITLE'", "name": "SingleMuPt10_cfi", "immutable": false, "parameters": [{"flag": "--fileout", "value": "file:B2G-Summer12-00460.root"}, {"flag": "--eventcontent", "value": "RAWSIM"}, {"flag": "--datatier", "value": "GEN-SIM"}, {"flag": "--conditions", "value": "auto:startup"}, {"flag": "--python_filename", "value": "B2G-Summer12-00460_1_cfg.py"}, {"flag": "--no_exec", "value": ""}, {"flag": "--relval", "value": "25000,500"}], "type": "default"}' http://localhost:8000/api/steps;


STEP_ID=`curl -X GET -i -s -H "Accept: application/json"  'http://localhost:8000/api/steps?search='$STEP_TITLE | tr , "\n" | grep id | sed 's/"id": "\([^"]*\).*/\1/' | sed 's/ //g'`


curl -X POST -H "Content-Type: application/json" -d '{"label": "working-request-runTheMatrix-20", "description": "This request should work for testing", "type": "MC", "immutable": false, "steps": [{"id":'$STEP_ID'}], "cmssw_release": "CMSSW_5_3_11_patch2"}' http://localhost:8000/api/requests;

