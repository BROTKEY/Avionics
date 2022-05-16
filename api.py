import json
from sqlite3 import DatabaseError
from flask import Flask
import threading
import socket
import datetime
from flask_cors import CORS, cross_origin

ALLDATA = []
ALLDATA.append([])
ALLDATA.append([])
ALLDATA.append([])

def BMPAdapter():
    global ALLDATA
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 691))
    while True:
        data, addr = sock.recvfrom(1024)
        ALLDATA[0].append([str(data, 'UTF-8').split(","), str(datetime.datetime.now())])
        if len(ALLDATA[0]) > 99:
            ALLDATA[0] = ALLDATA[0][-99:]

def BNOAdapterEuler():
    global ALLDATA
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 692))
    while True:
        data, addr = sock.recvfrom(30)
        ALLDATA[1].append([str(data, 'UTF-8').split(","), str(datetime.datetime.now())])
        if len(ALLDATA[1]) > 99:
            ALLDATA[1] = ALLDATA[1][-99:]

def BNOAdapterAccel():
    global ALLDATA
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 693))
    while True:
        data, addr = sock.recvfrom(1024)
        ALLDATA[2].append([str(data, 'UTF-8').split(","), str(datetime.datetime.now())])
        if len(ALLDATA[2]) > 99:
            ALLDATA[2] = ALLDATA[2][-99:]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def SendData():
    return json.dumps(ALLDATA)

@app.route("/launch")
@cross_origin()
def launch():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes("start","utf-8"), ("192.168.43.100", 694))
    return "0"

if __name__ == "__main__":
    thread = threading.Thread(target=BMPAdapter)
    thread.start()
    thread = threading.Thread(target=BNOAdapterEuler)
    thread.start()
    thread = threading.Thread(target=BNOAdapterAccel)
    thread.start()
    
    app.run()