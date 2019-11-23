#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

git pull
./scripts/start_server.sh
