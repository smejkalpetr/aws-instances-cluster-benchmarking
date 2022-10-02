CXX = g++
CXXFLAGS = -Wall -pedantic
CPPFLAGS = -std=c++17

BIN = ./bin/
SRC = ./src/

all: compile run

compile: mkdir setup

setup:
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(SRC)setup.cpp -o $(BIN)setup.bin

mkdir:
	mkdir -p $(BIN)

run:
	chmod +x $(BIN)setup.bin
	$(BIN)setup.bin

clean:
	rm -rf $(BIN)
	