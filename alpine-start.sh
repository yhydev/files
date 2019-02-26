#!/bin/sh


sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
apk update && apk add docker ttyd nginx bash
pip install flask
mkdir /run/nginx/ && touch /run/nginx/nginx.pid 
cp default.conf /etc/nginx/conf.d/default.conf
python app.py
nginx
