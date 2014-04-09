


for i in {1..80}; do 

	rem=$(( $i % 2 ))
	
	if [ $rem -eq 0 ];
	then
	  immutable='true'
	else
	  immutable='false'
	fi

	curl -X POST -H "Content-Type: application/json" -d '{"label": "'$i'-req-label", "description": "test-description", "type": "MC", "immutable": '$immutable', "steps": [{"id": '$i'}, {"id": '$(($i + 1))'}]  }' http://localhost:8000/api/requests; 

done;

curl -X POST -H "Content-Type: application/json" -d '{"label": "working-testing", "description": "This request should work for testing", "type": "MC", "immutable": false, "steps": [{"id": 101}], "cmssw_release": "CMSSW_5_3_11_patch2"}' http://localhost:8000/api/requests;
