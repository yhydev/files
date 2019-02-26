import requests, logging
from flask import Flask, request, make_response
logging.basicConfig(level = logging.INFO)
app = Flask(__name__)


HEADER_SERVER = "CCAV"

@app.route("/host/<hostname>")
def host(hostname):
        logging.info("host() http")
        logging.info("hostname: %s" % hostname)

        resp = requests.request(request.method, "http://%s/" % hostname)
        
        logging.info(resp.content)
        response = make_response(resp.content, resp.status_code)
        response.headers["server"] = HEADER_SERVER
        for k, v in resp.headers.items():
                response.headers[k] = v
        return response


@app.route("/host/<hostname>/ws")
def ws(hostname):
        logging.info("host() ws")
        logging.info("hostname: %s" % hostname)

        resp = requests.request(request.method, "ws://%s/" % hostname)
        
        logging.info(resp.content)
        response = make_response(resp.content, resp.status_code)
        response.headers["server"] = HEADER_SERVER
        for k, v in resp.headers.items():
                response.headers[k] = v
        return response




app.run(host = "0.0.0.0", debug = True)




sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories\
&&apk update && apk add docker ttyd nginx bash vim\
&&pip install flask \
&&mkdir /run/nginx/ && touch /run/nginx/nginx.pid


