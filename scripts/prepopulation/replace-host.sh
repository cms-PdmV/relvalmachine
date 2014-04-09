#!/bin/bash


if [[ $# -ne 2 ]]; then
    echo "Illegal number of parameters. Pass two arguments: old hostname and new hostname"
    exit 1;
fi

HOST1=$1
HOST2=$2

echo $HOST1
echo $HOST2

sed -i 's/'$HOST1'/'$HOST2'/g' populate-*

#sed -i 's/cms-pdmv-rvmdev.cern.ch/localhost:8000/g' populate-*
