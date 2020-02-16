#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

git pull
echo "You need to migrate config.json and auth.json manually now."
read -p "Press enter when done"
./scripts/start_server.sh
