#!/bin/bash

set -e
set -x

sudo add-apt-repository -y ppa:costamagnagianfranco/borgbackup
sudo apt-get update
sudo apt-get install -y fakeroot borgbackup

pip install 'virtualenv'
python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements.d/development.txt
pip install codecov
pip install -e .
