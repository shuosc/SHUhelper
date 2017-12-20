#!/bin/bash   
cd UHE-frontend-quasar
mkdir ios
yarn install
yarn build ios
mv dist/* ios
yarn build
mkdir dist/ios
mv ios dist