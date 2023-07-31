#!/bin/bash

echo 'bak db'

mysqldump -uroot -phuya123456 -P3307 -h172.24.174.27 huya > huya.sql
echo 'bak db success'

docker-compose -f /root/docker-compose.yaml down
echo 'stop success'