import zerodb
import transaction
import models 
from random import choice, randint
from string import digits
import argparse
import subprocess
import time

#argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("IP")
parser.add_argument("dbsize", type=int)
parser.add_argument("elementsize", type=int)
parser.add_argument("distribution")
parser.add_argument("element")
args = parser.parse_args()

dbsize = args.dbsize
elementsize = args.elementsize
distribution = args.distribution
ip = args.IP
element = args.element

#server credentials
username = "root"
passphrase = "root"
certificate = "conf/server.pem"

#prepare random data
roomIDs = []
randomID = int(''.join(choice(digits) for j in range(4)))
for i in range(150):
    while(randomID in roomIDs):
        randomID = int(''.join(choice(digits) for j in range(4)))
    roomIDs.append(randomID)

nodeIDs = []
randomID = int(''.join(choice(digits) for i in range(5)))
for i in range(900):
    while(randomID in nodeIDs):
        randomID = int(''.join(choice(digits) for j in range(5)))
    nodeIDs.append(randomID)

#connect to server
db = zerodb.DB((ip, 8001), username=username, password=passphrase, server_cert=certificate)

#fill it with data
if (element == "Measurement"):
    for j in range(int(dbsize/100)):
        timenow = time.time()
        with transaction.manager:
            for i in range(100):
                roomID=choice(roomIDs)
                roomIDindex = roomIDs.index(roomID)
                print(roomID)
                e = models.Measurement(roomID=roomID, nodeID=choice(nodeIDs[roomIDindex*6:roomIDindex*6+6]), value=randint(0,500), date=timenow)
                db.add(e)
elif (element == "State"):
    for j in range(int(dbsize/100)):
        with transaction.manager:
            for i in range(100):
                roomID=choice(roomIDs)
                roomIDindex = roomIDs.index(roomID)
                e = models.State(roomID=roomID, nodeID=choice(nodeIDs[roomIDindex*6:roomIDindex*6+6]), desc="door"+"."*elementsize, state=choice(range(0, 4)))
                db.add(e)
#finish
db.disconnect()
print("Server Population done")
