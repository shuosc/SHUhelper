#!/bin/bash   
cd web
mkdir ios
yarn install
yarn build ios
mv dist/* ios
yarn build
mkdir dist/ios
mv ios dist
rm -r pub/*
cp -r dist/* pub