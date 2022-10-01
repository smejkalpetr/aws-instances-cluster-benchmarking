#!/bin/bash

# read key pair name
read -p "Enter key pair name (including the .pem extension!): " MY_AWS_KEYPAIR_NAME

# create a new AWS key pair
aws ec2 create-key-pair --key-name '$MY_AWS_KEYPAIR_NAME' --query 'KeyMaterial' --output text > '$MY_AWS_KEYPAIR_NAME'
