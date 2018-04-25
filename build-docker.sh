#!/usr/bin/env bash

# Bring up local environment

#docker-machine create -d vmwarefusion travisci

#eval $(docker-machine env travisci)

# Build image, tag as storyboardgenerator-repo
# optionally use --no-cache=true

docker build -t storyboardgenerator-repo .

# Run locally
docker run -p 80:80 -t storyboardgenerator-repo

