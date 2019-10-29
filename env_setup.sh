#!/bin/bash

mkdir PyEnv
cd PyEnv
sudo apt install python3-venv
python3 -m venv .
source bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

