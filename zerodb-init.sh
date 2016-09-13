#!/bin/bash
# Author=Elias Hazboun
# A script to create config files of zeroDB
# Deletes old database instance
# usage zerodb-init.sh IP

if [ $# -lt 1 ]
then
    echo "error: missing arguments"
    exit -1
elif [ $# -gt 1 ]
then 
    echo "ignoring extra arguments"
fi
rm -rf conf db
#zerodb-manage init_db
./script.exp
sed -i -- "s/localhost/$1/g" conf/server.conf
scp ./conf/server.pem ilab@pc1:/home/ilab/zerodb/
exit 0
