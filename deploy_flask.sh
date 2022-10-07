#!/bin/bash

instanceId=$(ec2metadata --instance-id)

# install pip3 and venv
sudo apt update;
sudo apt install -y python3-pip;
sudo apt install -y python3-venv;

# this is to be able to bind to port 80 without sudo
# source: https://gist.github.com/justinmklam/f13bb53be9bb15ec182b4877c9e9958d
sudo apt install -y authbind
sudo touch /etc/authbind/byport/80
sudo chmod 777 /etc/authbind/byport/80

# create directory for the app
mkdir flaskApp && \
cd flaskApp

# create new venv
python3 -m venv venv

# activate the venv & install flask in it
source venv/bin/activate
pip3 install flask

# create file with the actual flask app code
cat <<EOF > /home/ubuntu/flaskapp.py
from flask import Flask
app = Flask(__name__)

@app.route('/cluster')
def hello_world():
    return '[VM RESPONSE] Flask app running on VM with ID $instanceId is responding...'
EOF

# export required variable and run the flask app
export FLASK_APP=/home/ubuntu/flaskapp.py
authbind --deep flask run --host 0.0.0.0 --port 80
