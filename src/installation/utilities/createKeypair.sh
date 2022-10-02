#!/bin/bash

# read key pair name
echo "###>>>>---------------<<<<###"
echo "Creating new Key Pair..."

read -p "Enter key pair name: " MY_AWS_KEYPAIR_NAME

# create a new AWS key pair
echo "The new key pair is being created (with suitable rules)..."
aws ec2 create-key-pair --key-name "$MY_AWS_KEYPAIR_NAME" --query 'KeyMaterial' --output text > "${MY_AWS_KEYPAIR_NAME}.pem" && \
echo "Your new keypair has been saved at the /src/installation/utilities folder."
echo ""