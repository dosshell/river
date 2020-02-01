#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker login registry.gitlab.com
docker push registry.gitlab.com/dosshell/river:latest
