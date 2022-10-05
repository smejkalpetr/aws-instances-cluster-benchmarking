#!/bin/bash

# #::: installPythonAndFlask.sh :::#
# This script installs python and the python framework

# install python
apt-get update
apt-install python3
#install venv module
apt-install python3-venv
#create folder and open it
mkdir flask_application
cd flask_application
#create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
#install flask
y | pip install Flask
#the python file should be inserted in this folder, not sure how to do this
FLASK_APP=VMinstance.py flask run -p 80
