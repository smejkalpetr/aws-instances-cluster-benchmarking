#!/bin/bash

if [ $# -eq 0 ];
then
    echo "$0: Missing arguments"
    exit 1
elif [ $# -gt 2 ];
then
    echo "$0: Too many arguments: $@"
    exit 1
else
    if [ "$1" == "install" ];
    then
        echo "Installing..."
        mkdir -p ./keys/ ;
        virtualenv venv && \
    	source venv/bin/activate && \
    	pip install -r requirements.txt;
    f
    elif [  "$1" == "run" ];
    then
        echo "Running..."
        python3 ./pyt/main.py
    elif [  "$1" == "clean" ];
    then
        echo "Cleaning..."
        rm -rf ./venv
    elif [  "$1" == "deactivate" ];
    then
        echo "Deactivating..."
        deactivate
    elif [  "$1" == "activate" ];
    then
        echo "Activating..."
        source venv/bin/activate
    else
        echo "Wrong argument."
    fi
fi
