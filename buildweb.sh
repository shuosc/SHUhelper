#!/bin/bash   
cd Web
mkdir pub
mkdir ios
yarn install
yarn build ios
mv dist/* ios
yarn build
mkdir dist/ios
mv ios dist
mv dist/* pub