


for i in {0..400}; do 

	rem=$(( $i % 2 ))
	
	if [ $rem -eq 0 ];
	then
	  immutable='true'
	else
	  immutable='false'
	fi
	curl -X POST -H "Content-Type: application/json" -d '{"title": "'$i'-blob-title", "immutable": '$immutable', "parameters": [{"flag": "--eventcontent", "value":"RAW"}, {"flag": "--slhc", "value": "test"}] }' http://localhost:8000/api/predefined_blob; 

done;
