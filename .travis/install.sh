#!/bin/bash

set -e
set -x

sudo add-apt-repository -y ppa:costamagnagianfranco/borgbackup
sudo apt-get update

is_xenial=$(lsb_release -r | grep 16.04 &>/dev/null && echo "y" || echo "n")

sudo apt-get install -y fakeroot

if [ "$is_xenial" = "y" ]; then
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
