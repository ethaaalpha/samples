#!/bin/bash

set -e

# default jackett folder
mkdir -p /config/Jackett/Indexers
cp indexers/* /config/Jackett/Indexers

# for apikey
envsubst < config.template.json > /config/Jackett/ServerConfig.json

# to keep pid_1
exec /init
