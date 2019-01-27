#!/usr/bin/env bash

docker-compose pull
# 目前暂无需要持久化的数据
docker-compose up -d --force-recreate mongodb
docker-compose up -d --force-recreate redis
sleep 10
docker-compose up -d --force-recreate backend
docker-compose up -d --force-recreate frontend