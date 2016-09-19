import subprocess
import argparse
import os
import statistics

#argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

input_file = args.input

subprocess.call(['tshark', '-r', input_file, '-w', 'temp.pcapng', '-d', 'tcp.port==8001,ssl', '-Y', "tcp.port eq 8001", '-Y', 'ssl'])
data=subprocess.check_output(['tshark', '-r', 'temp.pcapng', '-Y', 'ssl', '-T', 'fields', '-d', 'tcp.port==8001,ssl', '-e', 'ip.src', '-e', 'frame.time_delta']).decode("utf-8")
list=[line.split("\t") for line in data.splitlines()]

server="192.168.38.4"
client="192.168.38.1"
oldSource=list[0][0]
counter=0
serverTime=[]
clientTime=[]
clientReplies=0
serverReplies=0
accumulatedDelta=0
for i in range(len(list)):
    if(list[i][0]!=oldSource):
        counter=counter+1
        oldSource=list[i][0]
        if(list[i][0]==server):
            serverTime.append(float(list[i][1]))
        else:
            clientTime.append(float(list[i][1]))
    else:
        accumulatedDelta=accumulatedDelta+float(list[i][1])
        
data=subprocess.check_output(['./stats.sh', 'temp.pcapng']).decode("utf-8")
stats=data.split()
print("client max response time = {0:.8f}, min = {1:.8f}, average = {2:.8f}, variance = {3:.8f}, median = {4:.8f}".format(max(clientTime),min(clientTime),statistics.mean(clientTime),statistics.pvariance(clientTime),statistics.median(clientTime)))
print("server max response time = {0:.8f}, min = {1:.8f}, average = {2:.8f}, variance = {3:.8f}, median = {4:.8f}".format(max(serverTime),min(serverTime),statistics.mean(serverTime),statistics.pvariance(serverTime),statistics.median(serverTime)))
print("{0} client messages({1}B) and {2} server messages({3}B), organized into {4} request/reply roundtrips in {5} seconds (total= {6} messages({7}B)".format(stats[2],stats[3],stats[0],stats[1],counter,stats[4],stats[6],stats[5]))
os.remove('temp.pcapng')
