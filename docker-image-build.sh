#!/bin/bash

VERSION=$1

docker build --build-arg VERSION=$VERSION --build-arg USER=$DOCKER_USER_ID \
       -t "${DOCKER_USER_ID}/common-validations:latest" \
       -t "${DOCKER_USER_ID}/common-validations:${VERSION}" .
docker push "${DOCKER_USER_ID}/common-validations:${VERSION}"
docker push "${DOCKER_USER_ID}/common-validations:latest"
