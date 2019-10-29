#!/bin/bash

set -e
set -x

sudo add-apt-repository -y ppa:costamagnagianfranco/borgbackup
sudo apt-get update
sudo apt-get install -y fakeroot borgbackup

# Chicken/egg problem with Python 3.8... current Travis pip is not
# compatible with Python 3.8, but we need a newer one to fix it...
# Solution: install pip the "manual" way so that we can bootstrap.
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --no-setuptools --no-wheel

pip install 'virtualenv<14.0'
python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements.d/development.txt
pip install codecov
pip install -e .
