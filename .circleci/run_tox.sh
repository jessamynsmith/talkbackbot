#!/bin/bash

# This script will quit on the first error that is encountered.
set -e

for version in "$@"
do
    export PATH="$HOME/.pyenv/versions/$version/bin":$PATH
done

tox
