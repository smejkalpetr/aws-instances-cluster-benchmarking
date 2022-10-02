#!/bin/bash

# #::: createKeyPair.sh :::#
# This script creates a Key Pair with given name and saves the corresponding private key.

# create a new AWS key pair
aws ec2 create-key-pair --key-name "$1" --query 'KeyMaterial' --output text > "${1}.pem"

