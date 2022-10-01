#!/bin/bash

# read key pair name
read -p "Enter key pair name (with .pem extension!): " MY_AWS_KEYPAIR_NAME

aws ec2 create-key-pair --key-name '$MY_AWS_KEYPAIR_NAME' --query 'KeyMaterial' --output text > "$MY_AWS_KEYPAIR_NAME"