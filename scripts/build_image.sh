#!/bin/sh

MY_PATH="`dirname \"$0\"`"
cd $MY_PATH/..

docker build -t registry.gitlab.com/dosshell/river:latest .
