#!/bin/env python
#coding=utf-8

from flask import Flask, jsonify, make_response
import os, re, time, socket, sys

app = Flask(__name__)

SO_BINDTODEVICE=25
BASE_DIRNAME = os.path.dirname(sys.argv[0])
INDEX_PATHNAME = os.path.join(BASE_DIRNAME, "index.html")

def getFreePort(iface=None):
    s = socket.socket()

    if iface:
        s.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, bytes(iface,'utf8'))

    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()

    return port


@app.route("/linux")
def createLinux():

        logfilename = "/tmp/share-linux-%s.log" % str(1000 * time.time())
        port = getFreePort()
        cmd = "nohup  ttyd -I %s -p %d docker run -it ubuntu bash > %s 2>&1 &" % (INDEX_PATHNAME, port, logfilename)
        os.system(cmd)
        return jsonify({"port": port})


if __name__ == '__main__':
        app.run(host = "0.0.0.0")
