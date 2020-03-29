#!/bin/sh

docker login registry.gitlab.com
docker push registry.gitlab.com/dosshell/river:latest

