#!/bin/bash

# run this file on the server to update to latest

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

git pull
./scripts/build_push_image.sh
./scripts/update_container.sh

