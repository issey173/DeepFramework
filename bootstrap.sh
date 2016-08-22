#!/usr/bin/env bash

## Install PIP
sudo apt-get install -y python-pip

## Install virtualenvwrapper
sudo pip install virtualenvwrapper
# Add the initialization script to .bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
# Execute the initialization script
source /usr/local/bin/virtualenvwrapper.sh
# Create the virtualenv
mkvirtualenv dframe
# Init the virtualenv on login
echo "workon dframe" >> ~/.bashrc

## Install pip dependencies
cd /vagrant
# Install requirements.txt
pip install -r requirements.txt