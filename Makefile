SHELL := /bin/bash

VENV = ./venv/
KEYS = ./keys/

all: mkdir install run

install:
		virtualenv venv && \
    	source venv/bin/activate && \
    	pip install -r requirements.txt;

run:
	python3 ./pyt/main.py

mkdir: 
	mkdir -p $(KEYS)

stop:
	deactivate

clean:
	rm -rf $(VENV)
	
	