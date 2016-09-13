#!/bin/bash
# Author=Elias Hazboun
# A script to display statistics of capture files
# usage: analyze.sh path/to/files output file

if [ $# -lt 1 ]
then
    echo "error: missing arguments"
    exit -1
elif [ $# -gt 1 ]
then
    echo "ignoring extra arguments"
fi 


stats=$(tshark -q -z conv,ip,"tcp"  -r $1 | tail -2 | head -1)
serverPackets=$(echo $stats | awk '{print $4}')
serverBytes=$(echo $stats | awk '{print $5}')
clientPackets=$(echo $stats | awk '{print $6}')
clientBytes=$(echo $stats | awk '{print $7}')
duration=$(echo $stats | awk '{print $11}')
totalBytes=$(($serverBytes+$clientBytes))
totalPackets=$(($serverPackets+$clientPackets))

echo "$serverPackets $serverBytes $clientPackets $clientBytes $duration $totalBytes $totalPackets"
