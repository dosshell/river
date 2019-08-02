#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker login registry.gitlab.com
docker build -t registry.gitlab.com/dosshell/river:latest .
docker run --rm --name river-once -v $PWD/settings.json:/app/settings.json registry.gitlab.com/dosshell/river:latest --now
