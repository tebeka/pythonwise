#!/bin/bash

# Repository status

root=$PWD
while [ "$root" != "/" ];
do
    if [ -d "$root/.hg" ]; then
        hg status 
        break
    fi
    if [ -d "$root/.git" ]; then
        git status --untracked-files=no
        break
    fi
    if [ -d "$root/.svn" ]; then
        svn status
        break
    fi
    if [ -d "$root/.bzr" ]; then
        bzr status
        break
    fi
    root=$(dirname "$root")
done

if [ "$root" == "/" ]; then
    echo "error: can't find a repository here"
    exit 1
fi
