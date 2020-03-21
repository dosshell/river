#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker build -t registry.gitlab.com/dosshell/river:latest .
docker run \
	--rm \
	--name river-once \
	-e TZ='Europe/Stockholm' \
	-v $PWD/config.json:/app/config.json \
	-v $PWD/auth.json:/app/auth.json \
	-v $PWD/cache.db:/app/cache.db \
	registry.gitlab.com/dosshell/river:latest \
	"$@"

