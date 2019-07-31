#!/bin/bash

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker stop river
docker rm river
docker pull registry.gitlab.com/dosshell/river:latest
docker run --name river -v $PWD/settings.json:/app/settings.json --restart=unless-stopped -d registry.gitlab.com/dosshell/river:latest --mail
