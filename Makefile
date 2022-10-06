SHELL := /bin/bash

VENV = ./venv/
KEYS = ./keys/

all: mkdir install run

install:
		. ./setup.sh

run:
	python3 ./pyt/main.py

mkdir: 
	mkdir -p $(KEYS)

stop:
	deactivate

clean:
	rm -rf $(VENV)
	