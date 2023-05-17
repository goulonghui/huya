#!/bin/bash

set -e
echo build huya_app tag:$1
docker build -t huya_app:$1 -f ./docker/Dockerfile .
docker tag huya_app:$1 mrglh/huya_app:$1
docker push mrglh/huya_app:$1
echo push image mrglh/huya_app:$1 successfully!