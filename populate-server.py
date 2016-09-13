import zerodb  # ZeroDB itself
import transaction  # Transaction manager
import models  # ..and our data model
import argparse
import subprocess
import time

#argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("IP")
parser.add_argument("dbsize", type=int)
parser.add_argument("elementsize", type=int)
parser.add_argument("distribution")
args = parser.parse_args()

dbsize = args.dbsize
elementsize = args.elementsize
distribution = args.distribution
ip = args.IP

#server credentials
username = "root"
passphrase = "root"
certificate = "conf/server.pem"

#connect to server
db = zerodb.DB((ip, 8001), username=username, password=passphrase, server_cert=certificate)

#fill it with data
for j in range(int(dbsize/100)):
    timenow = time.time()
    with transaction.manager:
        for i in range(100):
            e = models.Measurement(mid="x"*elementsize, value=i*5, date=timenow)
            db.add(e)
#finish
db.disconnect()
print("Server Population done")
