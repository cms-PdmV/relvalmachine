#!/bin/bash

cd {{directory}}
find ./ -maxdepth 1 -type d  -ctime +{{days_to_keep_logs}} | xargs rm -rf
