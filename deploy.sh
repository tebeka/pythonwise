#!/bin/bash
# Deploy, meaning sync from last successful build

tag=last-green-build

# Fetch get the latest changes from remote but does not update working
# directory, just the index
git fetch --tags

# Merge to the last successful bulid
git merge ${tag}

# Tag currently deployed revision
git tag -f deployed ${tag}
git push --tags

