#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker stop river
docker rm river

docker build -t registry.gitlab.com/dosshell/river:latest .

docker run \
	--name river \
	-e TZ='Europe/Stockholm' \
	-v $PWD/config.json:/app/config.json \
	-v $PWD/auth.json:/app/auth.json \
	-v $PWD/cache.db:/app/cache.db \
	--restart=unless-stopped \
	-d \
	registry.gitlab.com/dosshell/river:latest \
	--config-file ../config.json \
	"$@"

