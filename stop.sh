#!/bin/bash

echo 'bak db'

mysqldump -uroot -phuya123456 -P3307 -h172.16.0.15 huya > huya.sql
echo 'bak db success'

docker-compose -f ./docker-compose.yaml down
echo 'stop success'