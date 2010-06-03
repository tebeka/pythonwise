#!/bin/bash

# Error on 1'st failure
set -e

tag=last-green-build
revision=$(git rev-parse HEAD)

echo "Tagging $commit as $tag"
git tag -f $tag $commit
git pull origin master
git push --tags origin master
