#!/bin/env python
#coding=utf-8

from flask import Flask, jsonify, url_for, render_template, request
import os, re, time, socket, sys, docker

app = Flask(__name__)

SO_BINDTODEVICE=25

#文件路径
BASE_DIRNAME = os.path.dirname(sys.argv[0])

#终端文件路径
INDEX_PATHNAME = os.path.join(BASE_DIRNAME, "terminal.html")

#容器最多个数
#MAX_CONTAINER = 8

#docker 接口
client = docker.from_env()


def getFreePort(iface=None):
    """获取一个免费端口"""
    s = socket.socket()

    if iface:
        s.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, bytes(iface,'utf8'))

    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()

    return port


@app.route("/api/v1/containers", methods = ["POST"])
def run():
        """
        Description:
        运行一个容器
        """
        logfilename = "/tmp/share-linux-%s.log" % str(1000 * time.time())
        image = "ubuntu"
        ret = None
        status = 200
        try:
            port = getFreePort()
            hostName = "share-linux-%d" % port
            container = client.containers.run(image, "sleep 2h", name = hostName, detach = True, remove = True)
            cmd = "nohup  ttyd -d 0 -I %s -p %d docker exec -it %s bash > %s 2>&1 &" % (INDEX_PATHNAME, port, hostName, logfilename)
            os.system(cmd)
            ret = jsonify({"port": port})
        except Exception as e:
            ret = str(e)
            status = 500
        
        return ret, status

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == '__main__':
        app.run(host = "0.0.0.0")
