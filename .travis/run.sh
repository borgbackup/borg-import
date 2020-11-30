#!/bin/bash

set -e
set -x

source ~/.venv/bin/activate

fakeroot -u tox -r
