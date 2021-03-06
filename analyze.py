import subprocess
import argparse
import os
import statistics
from xml.etree import ElementTree as et

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

root = et.Element('Measurement')

client = et.SubElement(root, "client")
response = et.SubElement(client, "response")
response.set('max', str(max(clientTime)))
response.set('min', str(min(clientTime)))
response.set('average', str(statistics.mean(clientTime)))
response.set('variance', str(statistics.pvariance(clientTime)))
response.set('median', str(statistics.median(clientTime)))
client.set('total', str(stats[2]))
client.set('totalBytes', str(stats[3]))

server = et.SubElement(root, "server")
response1 = et.SubElement(server, "response")
response1.set('max', str(max(serverTime)))
response1.set('min', str(min(serverTime)))
response1.set('average', str(statistics.mean(serverTime)))
response1.set('variance', str(statistics.pvariance(serverTime)))
response1.set('median', str(statistics.median(serverTime)))
server.set('total', str(stats[0]))
server.set('totalBytes', str(stats[1]))
root.set('total', str(stats[6]))
root.set('totalBytes', str(stats[5]))
root.set('roundTrips', str(counter))
root.set('time', str(stats[4].replace(',','.')))



f = open((os.path.splitext(input_file)[0])+".xml", 'w')
f.write(et.tostring(root, encoding='utf-8').decode('utf-8'))
f.close()
os.remove('temp.pcapng')

#print("client max response time = {0:.8f}, min = {1:.8f}, average = {2:.8f}, variance = {3:.8f}, median = {4:.8f}".format(max(clientTime),min(clientTime),statistics.mean(clientTime),statistics.pvariance(clientTime),statistics.median(clientTime)))
#print("server max response time = {0:.8f}, min = {1:.8f}, average = {2:.8f}, variance = {3:.8f}, median = {4:.8f}".format(max(serverTime),min(serverTime),statistics.mean(serverTime),statistics.pvariance(serverTime),statistics.median(serverTime)))
#print("{0} client messages({1}B) and {2} server messages({3}B), organized into {4} request/reply roundtrips in {5} seconds (total= {6} messages({7}B)".format(stats[2],stats[3],stats[0],stats[1],counter,stats[4],stats[6],stats[5]))
