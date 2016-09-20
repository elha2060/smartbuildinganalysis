#!/bin/bash
# Author=Elias Hazboun
# A script to capture network traffic


###########################################
#            BEGIN TEST SETTINGS          #
###########################################
bandwidthr=(10 100 1000)
latencyr=(1 10 100 1000)
querysizer=(1 10 100 1000 10000)
queryr=('select')
###########################################
#            END TEST SETTINGS            #
###########################################


if [ $# -lt 6 ]
then
    echo "error: missing arguments"
    exit -1
elif [ $# -gt 6 ]
then
    echo "ignoring extra arguments"
fi 

interface=$1
dbsize=$2
elementsize=$3
distribution=$4
element=$5
ip="$6"

#remove old server and create a new one bound to IP
./zerodb-init.sh "$ip"
#run new server instance on PC4
zerodb-server &
#get process ID
zerodb_PID=$!

#populate server instance
python3 populate-server.py $ip $dbsize $elementsize $distribution $element
for bandwidth in ${bandwidthr[*]}
do
	for latency in ${latencyr[*]}
	do
		for querysize in ${querysizer[*]}
		do
			if [ $querysize -gt $dbsize ]
			then
				continue
			fi 
			for query in ${queryr[*]}
			do
				output="$bandwidth-$latency-$dbsize-$elementsize-$query-$querysize-$distribution-$element.pcapng"
				#setup network settings
				sudo ./network-setup.sh $interface $latency $bandwidth
				#start traffic capture on PC4
				dumpcap -i $interface -w "$output" &
				#get process ID
				dumpcap_PID=$!
				sleep 1
				#start client on PC1
				ssh ilab@pc1 "python3 /home/ilab/scripts/client.py $ip $query $querysize $element"
				#end traffic capture
				kill $dumpcap_PID
				python3 analyze.py "$output"
			done
		done
	done
done
#shutdown server
kill $zerodb_PID
