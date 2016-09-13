import zerodb
from zerodb.query import *
from models import Measurement
import argparse


#argument parsing

parser = argparse.ArgumentParser()
parser.add_argument("IP")
parser.add_argument("query")
parser.add_argument("querysize", type=int)
parser.add_argument("element")
args = parser.parse_args()

query = args.query
querysize = args.querysize
element = args.element
ip = args.IP

#server credentials
username = "root"
passphrase = "root"

certificate = "/home/ilab/zerodb/server.pem"

#connect to server
db = zerodb.DB((ip, 8001), username=username, password=passphrase, server_cert=certificate)

johns = list(db[Measurement].all())
print(len(johns))
print(johns)
