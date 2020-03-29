#!/bin/sh

mydir="$(dirname "$0")"
rootdir="$(readlink -f "$mydir/../")"

error=false
if [ ! -f "$rootdir/config.json" ]; then
    echo "Error: No config.json file found."
    error=true
fi
if [ ! -f "$rootdir/auth.json" ]; then
    echo "Error: No auth.json file found."
    error=true
fi
if [ ! -f "$rootdir/cache.db" ]; then
    echo "Error: No cache.db file found"
    error=true
fi
if [ "$error" = true ]; then
    exit
fi

docker stop river
docker rm river

docker build -t registry.gitlab.com/dosshell/river:latest "$rootdir"

docker run \
    --name river \
    -e TZ='Europe/Stockholm' \
    --mount type=bind,src="$rootdir/config.json",dst="/app/config.json",readonly \
    --mount type=bind,src="$rootdir/auth.json",dst="/app/auth.json",readonly \
    --mount type=bind,src="$rootdir/cache.db",dst="/app/cache.db" \
    --restart=unless-stopped \
    -d \
    registry.gitlab.com/dosshell/river:latest \
    --config-file /app/config.json \
    --auth-file /app/auth.json \
    --cache-file /app/cache.db \
    --daemon \
    "$@"

