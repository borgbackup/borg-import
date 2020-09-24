#!/bin/bash

set -e
set -x

is_xenial=$(lsb_release -r | grep 16.04 &>/dev/null && echo "y" || echo "n")
is_focal=$(lsb_release -r | grep 20.04 &>/dev/null && echo "y" || echo "n")

if [ "$is_focal" = "n" ]; then
    # Only add PPA if we're not testing for Focal
    # We technically don't use the PPA for Xenial either, but keeping it for now should be OK
    sudo add-apt-repository -y ppa:costamagnagianfranco/borgbackup
fi

sudo apt-get update
sudo apt-get install -y fakeroot

if [ "$is_xenial" = "y" ] || [ "$is_focal" = "y" ]; then
    # Workaround for broken PPA
    sudo wget -O /usr/bin/borg https://github.com/borgbackup/borg/releases/download/1.1.11/borg-linux64
else
    sudo apt-get install -y borgbackup
fi

pip install 'virtualenv'
python -m virtualenv ~/.venv
source ~/.venv/bin/activate
pip install -r requirements.d/development.txt
pip install codecov
pip install -e .
