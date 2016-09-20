#!/bin/bash
# Author=Elias Hazboun
# A script to capture network traffic


###########################################
#            BEGIN TEST SETTINGS          #
###########################################
variables=('bandwidth' 'latency' 'dbsize' 'elementsize' 'query' 'querysize' 'distribution' 'element' 'ip')
elementr=(State Measurement)
dbsizer=(1000 10000 100000 500000)
elementsizer=(1 10 100 1000)
distributionr=('uniform')
ip="192.168.38.4"
interface='eth-man'
###########################################
#            END TEST SETTINGS            #
###########################################


kill $(ps aux | grep 'zerodb-server' | awk '{print $2}')
kill $(ps aux | grep 'dumpcap' | awk '{print $2}')

for element in ${elementr[*]} 
do
	for dbsize in ${dbsizer[*]}
	do
		for elementsize in ${elementsizer[*]}
		do 
			for distribution in ${distributionr[*]}
			do
				./analyze.sh $interface $dbsize $elementsize $distribution $element "$ip"
			done
		done
	done
done
