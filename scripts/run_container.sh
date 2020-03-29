#!/bin/sh

mydir="$(dirname "$0")"
rootdir="$(readlink -f "$mydir/../")"

mountconf=""
mountauth=""
if [ -f "$rootdir/config.json" ]; then
    mountconf="--mount type=bind,src="$rootdir/config.json",dst="/app/config.json",readonly"
else
    echo "Warning: No config.json file found to mount in container."
fi
if [ -f "$rootdir/auth.json" ]; then
    mountauth="--mount type=bind,src="$rootdir/auth.json",dst="/app/auth.json",readonly"
else
    echo "Warning: No auth.json file found to mount in container."
fi
if [ ! -f "$rootdir/cache.db" ]; then
    echo "Error: No cache.db file found. Execute \`touch cache.db\` to create a new empty cache in river root directory."
    exit
fi

docker build -t registry.gitlab.com/dosshell/river:latest "$rootdir"
docker run \
    --rm \
    --name river-once \
    -e TZ='Europe/Stockholm' \
    $mountconf \
    $mountauth \
    --mount type=bind,src="$rootdir/cache.db",dst="/app/cache.db" \
    registry.gitlab.com/dosshell/river:latest \
    "$@"

