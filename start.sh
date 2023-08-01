#!/bin/bash

mkdir -p /data/log

docker-compose pull
docker-compose -f ./docker-compose.yaml up -d


if [ -f huya.sql ]
then
  echo 'recover db'
  sleep 20s
  mysql -uroot -phuya123456 -P3307 -h172.16.0.15  huya < huya.sql
fi