#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker build -t registry.gitlab.com/dosshell/river:latest .
docker run \
	--rm \
	--name river-once \
	-e TZ='Europe/Stockholm' \
	-v $PWD/settings.json:/app/settings.json \
	registry.gitlab.com/dosshell/river:latest \
	"$@"
