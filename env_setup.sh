#!/bin/bash

mkdir PyEnv
cd PyEnv
sudo apt install python3-venv
python3 -m venv .
source bin/activate
pip3 install --upgrade pip
cd ..
pip3 install -r requirements.txt

echo
echo 
echo "VirtualEnv set up, run source PyEnv/bin/activate to start it."
