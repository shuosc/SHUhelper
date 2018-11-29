#!/usr/bin/env bash

mkdir ./data
mongod --dbpath ./data --port 4004 > mongod.log &
redis-server > redis.log &
yarn run dev
