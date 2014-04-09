#!/bin/bash

for i in {1..100}; do 

	rem=$(( $i % 2 ))
	
	if [ $rem -eq 0 ];
	then
	  immutable='true'
	else
	  immutable='false'
	fi


	curl -X POST -H "Content-Type: application/json" -d '{"title": "'$i'-step-title","name": "step-name-wro", "immutable": '$immutable', "parameters": [{"flag": "--datatier", "value":"GEN-SIM"}, {"flag": "--customise", "value": "Configuration/GlobalRuns/reco_TLR_42X.customisePPMC"}], "type": "default", "blobs": [{"id": '$i'}, {"id": '$(($i + 1))'}] }' http://localhost:8000/api/steps; 

done;
