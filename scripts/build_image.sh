#!/bin/sh

mydir="$(dirname "$0")"
cd $mydir/..

docker build -t registry.gitlab.com/dosshell/river:latest .

