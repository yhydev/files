#!/bin/sh

#sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

apk update && apk add docker ttyd nginx python3 curl

pipFileName=/tmp/get-pip.py

if [! -e $pipFileName];then
curl https://bootstrap.pypa.io/get-pip.py -o $pipFileName
python3 $pipFileName
fi

pip install flask

if [! -e "/run/nginx/nginx.pid"];then
	mkdir /run/nginx/ && touch /run/nginx/nginx.pid 
fi

cd `dirname $0`
cp default.conf /etc/nginx/conf.d/default.conf
cp index.html /var/lib/nginx/html/index.html
#nginx
#python3 app.py
