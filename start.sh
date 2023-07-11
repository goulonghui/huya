#!/bin/bash

mkdir -p /data/log

docker-compose pull
docker-compose -f /root/docker-compose.yaml up -d

sleep 20s
echo 'recover db'
mysql -uroot -phuya123456 -P3307 -h172.24.174.27  huya < huya.sql