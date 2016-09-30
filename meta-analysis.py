import subprocess
import argparse
import os
import statistics
from xml.etree import ElementTree as et
import re
import numpy as np
import pprint
import matplotlib.pyplot as plt

###########################################
#            BEGIN TEST SETTINGS          #
###########################################
bandwidthr = ['1','10','100','1000']
latencyr = ['1','10','100','1000']
querysizer = ['1','10','100','1000','10000']
queryr = ['select']
elementr = ['State','Measurement']
dbsizer = ['1000','10000','100000','500000']
elementsizer = ['1','10','100','1000']
distributionr = ['uniform']
###########################################
#            END TEST SETTINGS            #
###########################################

def analyze(files,results):
	roundtrips = []
	time = []
	totalBytes = []
	clientTime = []
	serverTime = []
	for file in files:
		e = et.parse(file).getroot()
		roundtrips.append(float(e.attrib.get('roundTrips')))
		time.append(float(e.attrib.get('time')))
		totalBytes.append(float(e.attrib.get('totalBytes')))
		client = e.find('client').find('response')
		clientTime.append(float(client.get('average')))
		server = e.find('server').find('response')
		serverTime.append(float(server.get('average')))
	results.append([statistics.mean(roundtrips),statistics.mean(time),statistics.mean(totalBytes),statistics.mean(clientTime),statistics.mean(serverTime)])

def draw(results,name,xlabel,ylabel,xaxis):
	plt.figure(1, figsize=(12,6))
	plt.subplot(231)
	plt.plot(xaxis,np.array(results)[:,0],'ro')
	plt.ylabel(ylabel[0])
	plt.xlabel(xlabel)
	plt.axis([min(map(float, xaxis)),max(map(float, xaxis)),min(np.array(results)[:,0])-10,max(np.array(results)[:,0])+10])

	plt.subplot(232)
	plt.plot(xaxis,np.array(results)[:,1])
	plt.ylabel(ylabel[1])
	plt.xlabel(xlabel)
	plt.axis([min(map(float, xaxis)),max(map(float, xaxis)),min(np.array(results)[:,1])-1,max(np.array(results)[:,1])+1])

	plt.subplot(233)
	plt.plot(xaxis,np.array(results)[:,2]/1024)
	plt.ylabel(ylabel[2])
	plt.xlabel(xlabel)
	plt.axis([min(map(float, xaxis)),max(map(float, xaxis)),min(np.array(results)[:,2]/1024)-50,max(np.array(results)[:,2]/1024)+50])

	plt.subplot(234)
	plt.plot(xaxis,np.array(results)[:,3])
	plt.ylabel(ylabel[3])
	plt.xlabel(xlabel)
	plt.axis([min(map(float, xaxis)),max(map(float, xaxis)),min(np.array(bandwidthresults)[:,3])-0.5,max(np.array(results)[:,3])+0.5])

	plt.subplot(235)
	plt.plot(xaxis,np.array(results)[:,4])
	plt.ylabel(ylabel[4])
	plt.xlabel(xlabel)
	plt.axis([min(map(float, xaxis)),max(map(float, xaxis)),min(np.array(results)[:,4])-0.5,max(np.array(results)[:,4])+0.5])
	plt.subplots_adjust(left=0.12, bottom=0.10, right=0.90, top=0.90, wspace=0.5, hspace=0.5)
	plt.savefig(name)
	plt.clf()


#argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("dir")
args = parser.parse_args()

dir = args.dir

bandwidthresults = []
latencyresults = []
querysizeresults = []
queryresults = []
elementresults = []
dbsizeresults = []
elementsizeresults = []
distributionresults = []

ylabel=['Roundtrips','Time in sec','Total Traffic in bytes','Client response time in sec','Server response time in sec']
for bandwidth in bandwidthr:
	files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r''+bandwidth+'-.*\.xml', f)]
	analyze(files,bandwidthresults)
draw(bandwidthresults,'Bandwidth.pdf','Bandwidth in Mbits',ylabel,bandwidthr)

for latency in latencyr:
	files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r'10+-'+latency+'-.*\.xml', f)]
	analyze(files,latencyresults)
draw(latencyresults,'Latency.pdf', 'Latency in sec',ylabel,latencyr)

for dbsize in dbsizer:
	files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r'10+-10*-'+dbsize+'-.*\.xml', f)]
	analyze(files,dbsizeresults)
draw(dbsizeresults,'DatabaseSize.pdf','Database Size in records',ylabel,dbsizer)

for elementsize in elementsizer:
	files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r'10+-10*-[15]0+-'+elementsize+'-.*\.xml', f)]
	analyze(files,elementsizeresults)
draw(elementsizeresults,'RecordSize.pdf','Record size in bytes',ylabel,elementsizer)
	
for querysize in querysizer:
	files = [os.path.join(dir, f) for f in os.listdir(dir) if re.match(r'10+-10*-[15]0+-10*-'+'|'.join(queryr)+'-'+querysize+'-.*\.xml', f)]
	analyze(files,querysizeresults)
draw(querysizeresults,'QuerySize.pdf','Records Queried',ylabel,querysizer)

#for query in queryr:
#	files = [f for f in os.listdir(dir) if re.match(r'10+-10*-[15]0+-10*-'+query+'-.*\.xml', f)]
#	analyze(files,queryresults)
#draw(queryresults,'query.pdf','Query Type',ylabel,queryr)

#for distribution in distributionr:
#	files = [f for f in os.listdir(dir) if re.match(r'10+-10*-[15]0+-10*-'+'|'.join(queryr)+'-10*-'+distribution+'-.*\.xml', f)]
#	analyze(files,distributionresults)
#draw(distributionresults,'distribution.pdf','Distribution',ylabel,distributionr)
	
#for element in elementr:
#	files = [f for f in os.listdir(dir) if re.match(r'.*-'+element+'\.xml', f)]
#	analyze(files,elementresults)
#draw(elementresults,'element.pdf','Records Type',ylabel,elementr)

