# Registrator

## Quick Start

## Run Reference


docker run -d --name=consul --net=host progrium/consul --server -bootstrap

docker run -d --name=registrator --net=host --volume=/var/run/docker.sock:/tmp/docker.sock gliderlabs/registrator:latest consul://localhost:8500

