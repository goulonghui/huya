#!/bin/bash

mkdir -p /data/log

docker-compose pull
docker-compose -f /root/docker-compose.yaml up -d