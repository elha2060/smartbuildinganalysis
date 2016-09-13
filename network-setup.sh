#!/bin/bash
# Author=Elias Hazboun
# A small script to create and delete rules for throttling and 
# modifying latency on an interface using tc
# usage: Clear rules: script clear interface
# usage: Add rule: script interface latency bandwidth
# latency in ms, bandwidth in Mbit

if [ $# -eq 2 ] && [ "$1" = "clear" ]
then
    interface=$2
    echo "deleting old tc configurations"
    tc qdisc del dev $interface root
    echo "done"
    exit 0
fi
if [ $# -lt 3 ]
then
    echo "error: missing arguments"
    exit -1
elif [ $# -gt 3 ]
then 
    echo "ignoring extra arguments"
fi
interface=$1
bit="Mbit"
ms="ms"
bandwidth=$3$bit
latency=$2$ms


old=$(tc class show dev eth-man)
if [ "$old" != "" ]
then
    echo "deleting old tc configurations"
    tc qdisc del dev $interface root
fi
echo "modifying $1 to have $2 ms latency and $3 Mbit bandwidth"
tc qdisc add dev $interface handle 1: root htb default 11
tc class add dev $interface parent 1: classid 1:1 htb rate 1000Mbps
tc class add dev $interface parent 1:1 classid 1:11 htb rate $bandwidth
tc qdisc add dev $interface parent 1:11 handle 10: netem delay $latency
echo "done."
exit 0
