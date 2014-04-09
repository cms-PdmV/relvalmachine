


for i in {1..40}; do 

	rem=$(( $i % 2 ))
	
	if [ $rem -eq 0 ];
	then
	  immutable='true'
	else
	  immutable='false'
	fi

	curl -X POST -H "Content-Type: application/json" -d '{"title": "'$i'-batch-title", "description": "test-description", "immutable": '$immutable', "requests": [{"id": '$i'}, {"id": '$(($i + 1))'}, {"id": '$(($i + 2))'}, {"id": '$(($i + 3))'}]  }' http://localhost:8000/api/batches; 

	
done;

for i in {1..5}; do

        rem=$(( $i % 2 ))

        if [ $rem -eq 0 ];
        then
          immutable='true'
        else
          immutable='false'
        fi

        curl -X POST -H "Content-Type: application/json" -d '{"title": "'$i'-batch-title-c", "description": "test-description", "immutable": '$immutable', "requests": [{"id": '$i'}, {"id": '$(($i + 1))'}, {"id": '$(($i + 2))'}, {"id": '$(($i + 3))'}], "run_the_matrix_conf": "-i -all -wm"  }' http://localhost:8000/api/batches;


done;

