#!/bin/env python
#coding=utf-8

from flask import Flask, jsonify
import os, re, time, socket, sys, docker

app = Flask(__name__)

SO_BINDTODEVICE=25
BASE_DIRNAME = os.path.dirname(sys.argv[0])
INDEX_PATHNAME = os.path.join(BASE_DIRNAME, "terminal.html")

def getFreePort(iface=None):
    s = socket.socket()

    if iface:
        s.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, bytes(iface,'utf8'))

    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()

    return port

client = docker.from_env()

@app.route("/<tag>")
def createLinux(tag = "ubuntu"):

        logfilename = "/tmp/share-linux-%s.log" % str(1000 * time.time())
        
        ret = None
        status = 200
        try:
            port = getFreePort()
            hostName = "share-linux-%d" % port
            container = client.containers.run(tag, "sleep 2h", name = hostName, detach = True, remove = True)
            cmd = "nohup  ttyd -I %s -p %d docker exec -it %s bash > %s 2>&1 &" % (INDEX_PATHNAME, port, hostName, logfilename)
            os.system(cmd)
            ret = jsonify({"port": port})
        except Exception as e:
            ret = str(e)
            status = 500
        
        return ret, status


if __name__ == '__main__':
        app.run(host = "0.0.0.0")
