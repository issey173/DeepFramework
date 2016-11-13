#!/usr/bin/env bash

## --------------------------- General stuff
sudo apt-get install -y nano
sudo apt-get install -y git

## --------------------------- PIP & Python
sudo apt-get -y update
sudo apt-get install -y python-pip
sudo pip install --upgrade pip

## --------------------------- Python dependencies
sudo pip install virtualenv
cd /home/vagrant
mkdir virtualenvs
cd virtualenvs
virtualenv dframe
source dframe/bin/activate
echo "source ~/virtualenvs/dframe/bin/activate" >> /home/vagrant/.bashrc
cd /vagrant
pip install -r requirements.txt
# Change virtualenv ownership
sudo chown vagrant /home/vagrant/virtualenvs/dframe -R