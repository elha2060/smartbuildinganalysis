#!/bin/bash
# Author=Elias Hazboun
# A script to capture network traffic

if [ $# -lt 3 ]
then
    echo "error: missing arguments"
    exit -1
elif [ $# -gt 3 ]
then
    echo "ignoring extra arguments"
fi 

interface=$1
output=$2
input=$3

#prepare an array to hold all variable from config file
declare -A config
#read config file into array
IFS="="
while read -r name value
do
config[$name]=$value
done < $input

#print config parameters
#for K in "${!config[@]}"; do echo $K --- ${config[$K]}; done


#remove old server and create a new one bound to IP
./zerodb-init.sh ${config[ip]}
#run new server instance on PC4
zerodb-server &
#get process ID
zerodb_PID=$!


#populate server instance
python3 populate-server.py ${config[ip]} ${config[dbsize]} ${config[elementsize]} ${config[distribution]} ${config[element]}
#setup network settings
sudo ./network-setup.sh $interface ${config[latency]} ${config[bandwidth]}
#start traffic capture on PC4
dumpcap -i $interface -w $output &
#get process ID
dumpcap_PID=$!
#start client on PC1
ssh ilab@pc1 "python3 /home/ilab/scripts/client.py ${config[ip]} ${config[query]} ${config[querysize]} ${config[element]}"
#end traffic capture
kill $dumpcap_PID
#shutdown server
kill $zerodb_PID
python3 analyze.py $output
