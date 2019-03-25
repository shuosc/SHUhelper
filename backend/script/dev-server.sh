#!/usr/bin/env bash

mkdir ./data
mongod --dbpath ./data --port 4004 > mongod.log &
redis-server > redis.log &

export JWT_SECRET=debug_jwt_secret
export ADMIN_TOKEN=debug_admin_secret
export MONGODB_ADDRESS=mongodb://localhost:4004
export REDIS_ADDRESS=redis://localhost:6379

npm run dev
